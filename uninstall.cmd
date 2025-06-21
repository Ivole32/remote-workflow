@echo off

set "BASE_PATH=%~1"
set "PYTHON_EXEC=%BASE_PATH%\python_no_venv.exe"
set "PYTHON_SCRIPT=.\uninstall.py"

set "PID=%~2"

:WAIT
timeout /t 2 >nul
tasklist /fi "PID eq %PID%" | find "%PID%" >nul
if not errorlevel 1 goto WAIT

start "" "%PYTHON_EXEC%" "%PYTHON_SCRIPT%"

exit /b