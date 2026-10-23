@echo off
cd /d "%~dp0\fly-new"
if not exist ".venv\Scripts\python.exe" (
  echo Python virtual environment not found.
  pause
  exit /b 1
)
echo Starting Flying Object Detection App...
".venv\Scripts\python.exe" -m streamlit run video_detection_app.py
if errorlevel 1 pause

