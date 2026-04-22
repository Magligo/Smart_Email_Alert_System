@echo off

echo 🔧 Setting up MailSense...

echo Creating virtual environment...
python -m venv venv

echo Activating environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo ✅ Setup complete! Now run main.py or run.bat
pause
