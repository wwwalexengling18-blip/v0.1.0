@echo off
setlocal
title A380 AI Crew - Control Center
cd /d "%~dp0"
if exist ".venv\Scripts\activate.bat" (
  call ".venv\Scripts\activate.bat"
)
python -m a380_ai_crew.control_center
cmd /k
