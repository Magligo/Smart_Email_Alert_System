@echo off
setlocal

set "BASE_DIR=%~dp0"
cd /d "%BASE_DIR%"

set "PYTHON_EXE=%BASE_DIR%venv\Scripts\python.exe"
set "SERVICE_SCRIPT=%BASE_DIR%service.py"

if not exist "%PYTHON_EXE%" (
    echo Virtual environment Python was not found in "%BASE_DIR%venv\Scripts".
    exit /b 1
)

"%PYTHON_EXE%" "%SERVICE_SCRIPT%" install
"%PYTHON_EXE%" "%SERVICE_SCRIPT%" start

endlocal
