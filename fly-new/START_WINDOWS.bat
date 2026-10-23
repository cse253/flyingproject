@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo First follow the installation steps in README_START_HERE.md.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m streamlit run video_detection_app.py
if errorlevel 1 pause
