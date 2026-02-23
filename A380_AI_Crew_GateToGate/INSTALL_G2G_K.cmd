@echo off
REM ============================================================
REM INSTALL_G2G_K.cmd  (Gate-to-Gate) - KEEP OPEN
REM - ASCII only, no line continuations
REM - creates .venv and installs project (editable) from pyproject.toml
REM ============================================================

if /I "%~1" NEQ "__keep" (
  start "A380 AI Crew (Install)" cmd /k "%~f0" __keep
  exit /b
)

setlocal EnableExtensions
cd /d "%~dp0"

echo === Python launcher ===
set "PYLAUNCH="
where py >nul 2>nul && set "PYLAUNCH=py -3"
if not defined PYLAUNCH (
  where python >nul 2>nul && set "PYLAUNCH=python"
)
if not defined PYLAUNCH (
  echo [ERROR] Python not found.
  goto :end
)

echo === venv ===
if not exist ".venv\Scripts\python.exe" (
  %PYLAUNCH% -m venv .venv
  if errorlevel 1 (
    echo [ERROR] venv create failed.
    goto :end
  )
)

set "PY=.venv\Scripts\python.exe"

echo === pip toolchain ===
"%PY%" -m pip install --upgrade pip setuptools wheel

echo === editable install ===
"%PY%" -m pip install -e .

echo.
echo OK - install done.
echo Next: run RUN_G2G_K.cmd
:end
endlocal
