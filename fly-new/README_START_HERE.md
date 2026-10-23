# Flying Object Detection - share package

1. Install Python 3.11 (the Python version used on the source computer).
2. Extract this entire ZIP before running; keep the model folder structure intact.
3. Open a terminal in the extracted Flying_Object_Detection folder and run:

   python -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements-video-engine.txt
   .venv\Scripts\python.exe -m streamlit run video_detection_app.py

On Windows, after installing dependencies, you can also double-click START_WINDOWS.bat.
On macOS/Linux use .venv/bin/python in place of .venv\Scripts\python.exe.

Open the local URL shown by Streamlit, upload a video, choose a pipeline,
and click Process video. Outputs are created in video_engine_outputs/.
All five classifier heads and the trained YOLO detector are included.

Internet is needed to install Python dependencies and to download the pretrained
MobileNetV3-Small backbone on first use. This is a Python source package, not a
standalone executable. CPU works; an NVIDIA GPU is optional. For GPU setup see
the PyTorch link in VIDEO_ENGINE_README.md.

Included: app, engine, dependency list, six trained checkpoints, GAN preview,
validation/test head scores, and usage documentation.
Excluded: datasets, training notebooks/caches, extra checkpoints, old archives,
and generated videos/results. The notebook mentioned in VIDEO_ENGINE_README.md
is training material and is not required or included in this runtime package.

See VIDEO_ENGINE_README.md for pipeline details and model limitations.
