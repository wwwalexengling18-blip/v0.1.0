@echo off
setlocal
title A380 AI Crew - Install (Gate-to-Gate)
cd /d "%~dp0"
echo === A380 AI Crew: venv + deps ===
if not exist ".venv" (
  py -3.12 -m venv .venv
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install -e .
echo.
echo Fertig. Starte jetzt: START_ControlCenter.cmd
echo.
cmd /k
