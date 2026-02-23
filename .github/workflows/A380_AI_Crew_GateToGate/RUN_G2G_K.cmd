@echo off
setlocal
title A380 AI Crew - Run CLI
cd /d "%~dp0"
if exist ".venv\Scripts\activate.bat" (
  call ".venv\Scripts\activate.bat"
)
python -m a380_ai_crew.cli run --plan configs\gate_to_gate.yaml
cmd /k
