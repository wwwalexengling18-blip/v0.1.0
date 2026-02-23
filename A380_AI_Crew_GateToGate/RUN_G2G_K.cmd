@echo off
REM ============================================================
REM RUN_G2G_K.cmd  (Gate-to-Gate) - KEEP OPEN
REM - ensures .venv exists
REM - ensures package import works (editable install OR PYTHONPATH=src fallback)
REM - runs the Cold&Dark -> Ready Takeoff plan
REM ============================================================

if /I "%~1" NEQ "__keep" (
  start "A380 AI Crew (Gate-to-Gate)" cmd /k "%~f0" __keep
  exit /b
)

setlocal EnableExtensions
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [INFO] .venv missing -> running INSTALL_G2G_K.cmd
  call "%~dp0INSTALL_G2G_K.cmd" __keep
)

set "PY=.venv\Scripts\python.exe"

REM Try import; if it fails, do an editable install again.
"%PY%" -c "import a380_ai_crew" >nul 2>nul
if errorlevel 1 (
  echo [INFO] Package not importable -> (re)install editable
  "%PY%" -m pip install --upgrade pip setuptools wheel
  "%PY%" -m pip install -e .
)

REM Fallback for src-layout (even if install fails for any reason)
set "PYTHONPATH=%CD%\src"

echo.
echo Running plan: Cold & Dark -> Ready Takeoff (real load times)
echo Tip: MSFS 2024 start, load FBW A380X, wait cockpit ready.
echo.

"%PY%" -m a380_ai_crew.cli run --plan src\a380_ai_crew\procedures\g2g.yaml --tick 5

echo.
echo Done.
endlocal
