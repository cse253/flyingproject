# Flying object video engine

This local Streamlit app accepts a user video, runs YOLO12 detection and ByteTrack tracking, classifies each detected crop with a selected saved head, overlays labels, and saves an annotated MP4 plus per-detection and per-track CSV files. It offers YOLO12 + CNN, YOLO12 + LSTM, YOLO12 + Transformer, YOLO12 + BiLSTM + Attention, and YOLO12 + GAN + Transformer.

## Checkpoints

By default the app loads the matching head checkpoint when you select a pipeline:

- `YOLO12_Hybrid_v2/YOLO12_Hybrid_Sequence_Run_v2/yolo12_balanced/weights/best.pt`
- One of `CNN.pt`, `LSTM.pt`, `Transformer.pt`, `BiLSTM_Attention.pt`, or `cGAN_Transformer.pt` in `YOLO12_Hybrid_v2/YOLO12_Hybrid_Sequence_Run_v2/`

The app reconstructs the same frozen torchvision MobileNetV3-Small feature extractor used during crop-classifier training. Its pretrained weights download from torchvision the first time the app runs if they are not already cached.

## Run on Windows

From the project folder, install the app dependencies and start Streamlit:

```powershell
py -m pip install -r requirements-video-engine.txt
py -m streamlit run video_detection_app.py
```

Then open the local Streamlit URL, select the hybrid pipeline, upload an MP4/MOV/AVI/MKV/M4V/WebM file, and click **Process video**. Defaults are confidence 0.10, image size 640, and every frame. These settings help retain small moving objects, but may take longer. The **Live detection preview** updates with bounding boxes and class labels as frames are processed. When processing finishes, the app displays one final classification for the whole video, calculated as a confidence-weighted vote across all detections. It also shows the complete annotated video and download links. Results also appear under `video_engine_outputs/`.

## Meaning and limits of the five options

- **YOLO12 + CNN:** YOLO boxes followed by the crop CNN class prediction.
- **YOLO12 + LSTM:** YOLO boxes followed by an LSTM that classifies the last four crop-feature and box-motion observations for each ByteTrack ID.
- **YOLO12 + Transformer:** YOLO boxes followed by the Transformer crop-feature head.
- **YOLO12 + BiLSTM + Attention:** YOLO boxes followed by a bidirectional LSTM with attention over the last four crop-feature and box-motion observations for each ByteTrack ID.
- **YOLO12 + GAN + Transformer:** YOLO boxes followed by the Transformer head trained with generated GAN features.

The Colab notebook [YOLO12_All_Hybrids_Sequence_Colab.ipynb](</D:/Flying%20object%20detection/YOLO12_All_Hybrids_Sequence_Colab.ipynb>) retrains the detector and all heads. The local app expects the results under `YOLO12_Hybrid_v2/YOLO12_Hybrid_Sequence_Run_v2/`. The split selection requires every partition to contain a four-frame sequence for every class. LSTM heads train on ordered source-video groups with box-center motion features. The dataset has no object track IDs, so training picks the largest same-class box per frame; ByteTrack supplies track IDs during video inference. This is approximate association. GAN-generated crops are experimental and should be visually checked in `gan_preview.png`; compare held-out results before claiming improvement. The detector and heads train separately, not jointly end-to-end.

For NVIDIA CUDA, install the PyTorch and torchvision builds that match the installed CUDA runtime before starting the app; see the official [PyTorch installation selector](https://pytorch.org/get-started/locally/). CPU inference works but will be slower.

## Output files

- `*_annotated.mp4`: processed video with tracker IDs, hybrid crop class, and YOLO class when the two disagree.
- `*_detections.csv`: frame/time, box coordinates, YOLO label/score, and selected head label/score.
- `*_classification.csv`: one final class for the whole video and its weighted vote share.

The notebook reports crop metrics for image heads and sequence metrics for temporal heads; neither is an end-to-end metric on user videos. The detector defaults to two epochs for a quick baseline. Review the generated preview and held-out metrics before relying on predictions.
