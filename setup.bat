@echo off
setlocal

echo Setting up MailSense...

REM Step 1: Create venv
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Step 2: Use venv python directly (IMPORTANT)
set "VENV_PYTHON=venv\Scripts\python.exe"

echo Using Python:
%VENV_PYTHON% --version

REM Step 3: Upgrade pip
echo Upgrading pip...
%VENV_PYTHON% -m pip install --upgrade pip

REM Step 4: Install dependencies
if exist requirements.txt (
    echo Installing from requirements.txt...
    %VENV_PYTHON% -m pip install -r requirements.txt
) else (
    echo Installing dependencies manually...
    %VENV_PYTHON% -m pip install plyer google-api-python-client google-auth-httplib2 google-auth-oauthlib
)

REM Step 5: Verify plyer
echo Verifying plyer installation...
%VENV_PYTHON% -m pip show plyer

echo.
echo ✅ Setup complete!
echo 👉 Run: venv\Scripts\python main.py OR run.bat
pause