from __future__ import annotations

import re
import tempfile
from datetime import datetime
from pathlib import Path

import streamlit as st
import torch
import cv2

from video_engine import HEAD_FILES, VideoDetectionEngine


APP_DIR = Path(__file__).resolve().parent
RUN_DIR = APP_DIR / "YOLO12_Hybrid_v2" / "YOLO12_Hybrid_Sequence_Run_v2"
DEFAULT_DETECTOR = RUN_DIR / "yolo12_balanced" / "weights" / "best.pt"
OUTPUT_DIR = APP_DIR / "video_engine_outputs"

HYBRID_LABELS = {
    "YOLO12 + CNN": "CNN",
    "YOLO12 + LSTM": "LSTM",
    "YOLO12 + Transformer": "Transformer",
    "YOLO12 + BiLSTM + Attention": "BiLSTM + Attention",
    "YOLO12 + GAN + Transformer": "GAN + Transformer",
}

st.set_page_config(page_title="Flying Object Video Detector", page_icon="🛸", layout="wide")
st.title("Flying Object Detection and Classification")
st.write("Upload a video and select one of the five saved YOLO12 + classifier-head pipelines.")
st.caption(
    "The detector and heads were trained as separate components and are combined at inference. "
    "LSTM and BiLSTM classify ordered crop features and tracked box-center movement across video frames. "
    "GAN + Transformer uses the Transformer head trained with synthetic crop augmentation; inspect the saved GAN preview and metrics before claiming a benefit. "
    "YOLO12 trained for two epochs; video-level accuracy has not been measured."
)


@st.cache_resource(show_spinner="Loading YOLO12 and crop classifier…")
def load_engine(detector_path: str, classifier_path: str, head_name: str) -> VideoDetectionEngine:
    return VideoDetectionEngine(detector_path, classifier_path, head_name=head_name)


with st.sidebar:
    st.header("Model and video settings")
    detector_path = st.text_input("YOLO12 checkpoint", str(DEFAULT_DETECTOR))
    pipeline_label = st.selectbox("Hybrid pipeline", list(HYBRID_LABELS))
    head_name = HYBRID_LABELS[pipeline_label]
    classifier_path = st.text_input(
        "Classifier checkpoint", str(RUN_DIR / HEAD_FILES[head_name]), key=f"classifier_path_{head_name}",
        help="Defaults to the matching saved head. Change only if your checkpoint is elsewhere.",
    )
    confidence = st.slider("YOLO confidence threshold", 0.01, 0.90, 0.10, 0.01)
    image_size = st.select_slider("Inference image size", options=[320, 416, 512, 640], value=640)
    frame_stride = st.select_slider(
        "Process every Nth frame", options=[1, 2, 3, 5, 10], value=1,
        help="Larger values run faster. The annotated output keeps the original video frame rate.",
    )
    device_name = "CUDA GPU" if torch.cuda.is_available() else "CPU"
    st.caption(f"Inference device: {device_name}")

video_file = st.file_uploader(
    "Choose a video", type=["mp4", "mov", "avi", "mkv", "m4v", "webm"], accept_multiple_files=False
)

if video_file is not None:
    st.video(video_file)
    if st.button("Process video", type="primary", use_container_width=True):
        detector = Path(detector_path).expanduser()
        classifier = Path(classifier_path).expanduser()
        if not detector.is_file() or not classifier.is_file():
            st.error("Checkpoint not found. Check the model paths in the sidebar.")
            st.stop()

        safe_stem = re.sub(r"[^A-Za-z0-9_-]+", "_", Path(video_file.name).stem).strip("_") or "video"
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_output = OUTPUT_DIR / f"{safe_stem}_{run_id}"
        run_output.mkdir(parents=True, exist_ok=True)
        output_video = run_output / f"{safe_stem}_annotated.mp4"
        detections_csv = run_output / f"{safe_stem}_detections.csv"
        classification_csv = run_output / f"{safe_stem}_classification.csv"

        progress = st.progress(0.0)
        status = st.empty()
        st.subheader("Live detection preview")
        live_preview = st.empty()
        try:
            with tempfile.TemporaryDirectory(prefix="flying_video_") as temp_dir:
                input_path = Path(temp_dir) / (safe_stem + Path(video_file.name).suffix.lower())
                input_path.write_bytes(video_file.getbuffer())
                engine = load_engine(str(detector.resolve()), str(classifier.resolve()), head_name)

                def update_progress(frame: int, total: int) -> None:
                    ratio = min(frame / max(total, 1), 1.0)
                    progress.progress(ratio)
                    status.write(f"Processing frame {frame:,} of {total:,}…")

                def update_preview(frame, frame_index: int, total: int) -> None:
                    preview = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    preview_height, preview_width = preview.shape[:2]
                    if preview_width > 960:
                        new_height = round(preview_height * 960 / preview_width)
                        preview = cv2.resize(preview, (960, new_height))
                    live_preview.image(
                        preview,
                        channels="RGB",
                        caption=f"Live detections — frame {frame_index + 1:,} of {total:,}",
                        use_container_width=True,
                    )

                summary = engine.process_video(
                    input_path,
                    output_video,
                    detections_csv,
                    classification_csv,
                    confidence=confidence,
                    image_size=int(image_size),
                    frame_stride=int(frame_stride),
                    progress_callback=update_progress,
                    preview_callback=update_preview,
                )
            progress.progress(1.0)
            status.success("Video processing finished.")
            st.session_state["latest_video_result"] = summary
            st.session_state["latest_video_output"] = str(output_video)
            st.session_state["latest_detection_csv"] = str(detections_csv)
            st.session_state["latest_classification_csv"] = str(classification_csv)
        except Exception as exc:
            status.empty()
            st.exception(exc)

if "latest_video_output" in st.session_state:
    out_path = Path(st.session_state["latest_video_output"])
    det_csv = Path(st.session_state["latest_detection_csv"])
    classification_csv = Path(st.session_state["latest_classification_csv"])
    if out_path.is_file():
        summary = st.session_state["latest_video_result"]
        st.subheader("Processed result")
        a, b, c = st.columns(3)
        a.metric("Final video classification", summary["final_class"])
        b.metric("Detections", summary["detections"])
        c.metric("Frames analyzed", f"{summary['sampled_frames']:,} / {summary['frames']:,}")
        st.caption(
            f"Final-class vote share across detections: {summary['final_class_vote_share']:.1%}. "
            "This is a weighted vote share, not a calibrated probability."
        )
        if summary["detections"] == 0:
            st.warning(
                "No objects passed the current confidence threshold. Try lowering it to 0.05, "
                "keep image size at 640, and make sure the object is visible in the sampled frames."
            )
        st.video(str(out_path))

        d1, d2, d3 = st.columns(3)
        d1.download_button("Download annotated video", out_path.read_bytes(), file_name=out_path.name, mime="video/mp4")
        d2.download_button("Download final classification CSV", classification_csv.read_bytes(), file_name=classification_csv.name, mime="text/csv")
        d3.download_button("Download detections CSV", det_csv.read_bytes(), file_name=det_csv.name, mime="text/csv")
        st.caption(f"Outputs are also saved locally in `{out_path.parent}`.")
