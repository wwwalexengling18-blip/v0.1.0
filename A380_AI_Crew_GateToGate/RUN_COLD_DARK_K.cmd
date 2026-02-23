@echo off
setlocal
title A380 AI Crew - Cold & Dark Only
cd /d "%~dp0"
if exist ".venv\Scripts\activate.bat" (
  call ".venv\Scripts\activate.bat"
)
python -m a380_ai_crew.cli run --plan configs\cold_dark_only.yaml
cmd /k
