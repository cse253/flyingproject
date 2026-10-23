"""YOLO12 video detection with one of the saved crop-classifier heads."""

from __future__ import annotations

import csv
from collections import deque
from pathlib import Path
from typing import Callable

import cv2
import numpy as np
import torch
from PIL import Image
from torch import nn
import torch.nn.functional as F
from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small
from torchvision.transforms import Compose, Normalize, Resize, ToTensor
from ultralytics import YOLO


CLASS_NAMES = ["airplane", "bird", "helicopter", "kite", "parachute", "UAV"]


class CropCNNHead(nn.Module):
    """Must match the CNN head used in YOLO12_Hybrid_10k_OneHour_Colab.ipynb."""

    def __init__(self) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(576, 128, 3, padding=1),
            nn.ReLU(),
            nn.Conv1d(128, 64, 3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1),
            nn.Flatten(),
            nn.Linear(64, 6),
        )

    def forward(self, tokens: torch.Tensor) -> torch.Tensor:
        return self.net(tokens.transpose(1, 2))


class LSTMHead(nn.Module):
    """Temporal head trained on 4-frame crop-feature and box-motion sequences."""
    def __init__(self, bidir: bool = False, attention: bool = False) -> None:
        super().__init__()
        self.rnn = nn.LSTM(580, 64, 1, batch_first=True, bidirectional=bidir)
        dim = 128 if bidir else 64
        self.att = nn.Linear(dim, 1) if attention else None
        self.fc = nn.Sequential(nn.LayerNorm(dim), nn.Linear(dim, 64), nn.ReLU(), nn.Dropout(.1), nn.Linear(64, 6))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        z, _ = self.rnn(x)
        z = (z * self.att(z).softmax(1)).sum(1) if self.att is not None else z.mean(1)
        return self.fc(z)


class TransformerHead(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.proj = nn.Linear(576, 128)
        self.pos = nn.Parameter(torch.zeros(1, 16, 128))
        layer = nn.TransformerEncoderLayer(128, 4, 256, .1, batch_first=True)
        self.enc = nn.TransformerEncoder(layer, 2, enable_nested_tensor=False)
        self.fc = nn.Linear(128, 6)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.fc(self.enc(self.proj(x) + self.pos).mean(1))


HEADS = {
    "CNN": CropCNNHead,
    "LSTM": LSTMHead,
    "Transformer": TransformerHead,
    "BiLSTM + Attention": lambda: LSTMHead(True, True),
    "GAN + Transformer": TransformerHead,
}
HEAD_FILES = {
    "CNN": "CNN.pt",
    "LSTM": "LSTM.pt",
    "Transformer": "Transformer.pt",
    "BiLSTM + Attention": "BiLSTM_Attention.pt",
    "GAN + Transformer": "cGAN_Transformer.pt",
}


class VideoDetectionEngine:
    def __init__(
        self,
        detector_checkpoint: str | Path,
        classifier_checkpoint: str | Path,
        head_name: str = "CNN",
        device: str | None = None,
    ) -> None:
        self.device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
        detector_checkpoint = Path(detector_checkpoint)
        classifier_checkpoint = Path(classifier_checkpoint)
        if not detector_checkpoint.is_file():
            raise FileNotFoundError(f"YOLO checkpoint not found: {detector_checkpoint}")
        if head_name not in HEADS:
            raise ValueError(f"Unknown hybrid head {head_name!r}; choose one of {list(HEADS)}")
        if not classifier_checkpoint.is_file():
            raise FileNotFoundError(f"{head_name} checkpoint not found: {classifier_checkpoint}")

        self.detector = YOLO(str(detector_checkpoint))
        names = self.detector.names
        detector_names = [names[i] if isinstance(names, dict) else names[i] for i in range(6)]
        normalized = [str(name).lower() for name in detector_names]
        expected = [name.lower() for name in CLASS_NAMES]
        if normalized != expected:
            raise ValueError(f"Detector class order {detector_names} does not match {CLASS_NAMES}")

        # The training notebook froze this pretrained backbone and saved only the CNN head.
        # The first launch downloads the same torchvision MobileNetV3-Small weights if uncached.
        self.backbone = mobilenet_v3_small(weights=MobileNet_V3_Small_Weights.DEFAULT).features
        self.backbone.to(self.device).eval()
        for parameter in self.backbone.parameters():
            parameter.requires_grad_(False)

        state = torch.load(classifier_checkpoint, map_location="cpu", weights_only=True)
        self.head_name = head_name
        self.classifier = HEADS[head_name]()
        self.classifier.load_state_dict(state)
        self.classifier.to(self.device).eval()
        self.crop_transform = Compose(
            [
                Resize((96, 96)),
                ToTensor(),
                Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
            ]
        )

    @torch.inference_mode()
    def _classify_crops(
        self,
        crops: list[Image.Image],
        boxes: list[np.ndarray],
        track_ids: list[int],
        frame_width: int,
        frame_height: int,
        histories: dict[int, deque],
    ) -> tuple[list[int], list[float]]:
        if not crops:
            return [], []
        batch = torch.stack([self.crop_transform(crop) for crop in crops]).to(self.device)
        features = self.backbone(batch)
        tokens = F.adaptive_avg_pool2d(features, (4, 4)).flatten(2).transpose(1, 2)
        if self.head_name in {"LSTM", "BiLSTM + Attention"}:
            pooled = tokens.mean(dim=1)
            temporal_rows = []
            for feature, box, track_id in zip(pooled, boxes, track_ids):
                x1, y1, x2, y2 = map(float, box)
                center = torch.tensor(
                    [(x1 + x2) / (2 * frame_width), (y1 + y2) / (2 * frame_height)],
                    dtype=feature.dtype,
                    device=self.device,
                )
                hist = histories.setdefault(int(track_id), deque(maxlen=4))
                delta = center - hist[-1][576:578] if hist else torch.zeros_like(center)
                hist.append(torch.cat([feature, center, delta]))
                row = list(hist)
                while len(row) < 4:
                    row.insert(0, row[0])
                temporal_rows.append(torch.stack(row))
            model_input = torch.stack(temporal_rows)
        else:
            model_input = tokens
        probabilities = self.classifier(model_input).softmax(dim=1)
        scores, labels = probabilities.max(dim=1)
        return labels.cpu().tolist(), scores.cpu().tolist()

    def process_video(
        self,
        input_video: str | Path,
        output_video: str | Path,
        detections_csv: str | Path,
        classification_csv: str | Path,
        *,
        confidence: float = 0.25,
        image_size: int = 416,
        frame_stride: int = 2,
        progress_callback: Callable[[int, int], None] | None = None,
        preview_callback: Callable[[np.ndarray, int, int], None] | None = None,
    ) -> dict:
        input_video = Path(input_video)
        output_video = Path(output_video)
        detections_csv = Path(detections_csv)
        classification_csv = Path(classification_csv)
        for path in (output_video, detections_csv, classification_csv):
            path.parent.mkdir(parents=True, exist_ok=True)
        if frame_stride < 1:
            raise ValueError("frame_stride must be at least 1")

        capture = cv2.VideoCapture(str(input_video))
        if not capture.isOpened():
            raise ValueError(f"Could not open video: {input_video}")
        fps = float(capture.get(cv2.CAP_PROP_FPS)) or 25.0
        total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter(
            str(output_video), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
        )
        if not writer.isOpened():
            capture.release()
            raise RuntimeError(f"Could not create output video: {output_video}")

        detection_rows: list[dict] = []
        video_scores = np.zeros(6, dtype=np.float64)
        frame_index = 0
        annotated_frame = None
        sampled_frames = 0
        temporal_histories: dict[int, deque] = {}
        try:
            while True:
                ok, frame = capture.read()
                if not ok:
                    break
                if frame_index % frame_stride == 0:
                    sampled_frames += 1
                    result = self.detector.track(
                        source=frame,
                        persist=True,
                        tracker="bytetrack.yaml",
                        conf=confidence,
                        imgsz=image_size,
                        device=0 if self.device.type == "cuda" else "cpu",
                        verbose=False,
                    )[0]
                    boxes = result.boxes
                    xyxy = boxes.xyxy.cpu().numpy() if boxes is not None else np.empty((0, 4))
                    det_classes = boxes.cls.int().cpu().tolist() if boxes is not None else []
                    det_scores = boxes.conf.cpu().tolist() if boxes is not None else []
                    track_ids = (
                        boxes.id.int().cpu().tolist()
                        if boxes is not None and boxes.id is not None
                        else [-(frame_index * 10000 + i + 1) for i in range(len(xyxy))]
                    )

                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(rgb)
                    crops: list[Image.Image] = []
                    crop_boxes: list[np.ndarray] = []
                    crop_track_ids: list[int] = []
                    valid_indices: list[int] = []
                    for i, (x1, y1, x2, y2) in enumerate(xyxy):
                        left = max(0, min(int(x1), width))
                        top = max(0, min(int(y1), height))
                        right = max(0, min(int(x2), width))
                        bottom = max(0, min(int(y2), height))
                        if right > left and bottom > top:
                            crops.append(pil_image.crop((left, top, right, bottom)))
                            crop_boxes.append(np.asarray([x1, y1, x2, y2], dtype=np.float32))
                            crop_track_ids.append(int(track_ids[i]))
                            valid_indices.append(i)
                    crop_labels, crop_scores = self._classify_crops(
                        crops, crop_boxes, crop_track_ids, width, height, temporal_histories
                    )
                    cnn_for_detection: dict[int, tuple[int, float]] = {
                        i: (label, score)
                        for i, label, score in zip(valid_indices, crop_labels, crop_scores)
                    }

                    annotated_frame = frame.copy()
                    for i, (box, detector_class, detector_score, track_id) in enumerate(
                        zip(xyxy, det_classes, det_scores, track_ids)
                    ):
                        x1, y1, x2, y2 = map(int, box)
                        hybrid_class, hybrid_score = cnn_for_detection.get(
                            i, (int(detector_class), float(detector_score))
                        )
                        track_key = int(track_id)
                        weight = max(float(detector_score), 0.01) * max(float(hybrid_score), 0.01)
                        video_scores[hybrid_class] += weight

                        color = (40, 210, 90) if hybrid_class == detector_class else (0, 165, 255)
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                        label = (
                            f"ID {track_key if track_key >= 0 else 'n/a'} "
                            f"{CLASS_NAMES[hybrid_class]} {hybrid_score:.2f}"
                        )
                        if hybrid_class != detector_class:
                            label += f" (YOLO: {CLASS_NAMES[int(detector_class)]})"
                        y_text = max(22, y1 - 8)
                        cv2.putText(
                            annotated_frame,
                            label,
                            (x1, y_text),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.55,
                            color,
                            2,
                            cv2.LINE_AA,
                        )

                        detection_rows.append(
                            {
                                "frame": frame_index,
                                "time_seconds": round(frame_index / fps, 3),
                                "track_id": track_key if track_key >= 0 else "untracked",
                                "x1": x1,
                                "y1": y1,
                                "x2": x2,
                                "y2": y2,
                                "yolo_class": CLASS_NAMES[int(detector_class)],
                                "yolo_confidence": round(float(detector_score), 5),
                                "hybrid_class": CLASS_NAMES[int(hybrid_class)],
                                "hybrid_confidence": round(float(hybrid_score), 5),
                            }
                        )

                    if preview_callback is not None:
                        preview_callback(annotated_frame, frame_index, total_frames)

                writer.write(annotated_frame if annotated_frame is not None else frame)
                frame_index += 1
                if progress_callback and (frame_index % 5 == 0 or frame_index == total_frames):
                    progress_callback(frame_index, total_frames)
        finally:
            capture.release()
            writer.release()

        with detections_csv.open("w", newline="", encoding="utf-8") as handle:
            fields = [
                "frame", "time_seconds", "track_id", "x1", "y1", "x2", "y2",
                "yolo_class", "yolo_confidence", "hybrid_class", "hybrid_confidence",
            ]
            writer_csv = csv.DictWriter(handle, fieldnames=fields)
            writer_csv.writeheader()
            writer_csv.writerows(detection_rows)

        detected_count = int(len(detection_rows))
        if video_scores.sum() > 0:
            final_index = int(video_scores.argmax())
            final_class = CLASS_NAMES[final_index]
            final_vote_share = float(video_scores[final_index] / video_scores.sum())
        else:
            final_class = "No object detected"
            final_vote_share = 0.0
        with classification_csv.open("w", newline="", encoding="utf-8") as handle:
            fields = ["video", "final_class", "final_class_vote_share", "detections"]
            writer_csv = csv.DictWriter(handle, fieldnames=fields)
            writer_csv.writeheader()
            writer_csv.writerow(
                {
                    "video": input_video.name,
                    "final_class": final_class,
                    "final_class_vote_share": round(final_vote_share, 5),
                    "detections": detected_count,
                }
            )

        return {
            "frames": frame_index,
            "sampled_frames": sampled_frames,
            "fps": fps,
            "detections": len(detection_rows),
            "final_class": final_class,
            "final_class_vote_share": round(final_vote_share, 5),
            "output_video": str(output_video),
            "detections_csv": str(detections_csv),
            "classification_csv": str(classification_csv),
        }
