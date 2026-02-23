@echo off
REM ============================================================
REM START_G2G_K.cmd - KEEP OPEN (one-click)
REM - runs install (if needed) and then runs the plan
REM ============================================================

if /I "%~1" NEQ "__keep" (
  start "A380 AI Crew (START)" cmd /k "%~f0" __keep
  exit /b
)

setlocal
cd /d "%~dp0"

call "%~dp0INSTALL_G2G_K.cmd" __keep
call "%~dp0RUN_G2G_K.cmd" __keep

endlocal
