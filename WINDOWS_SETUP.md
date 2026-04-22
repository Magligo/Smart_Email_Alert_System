# Windows Background Setup

This project already has the long-running loop in `main.py`, so the Windows setup below keeps your core logic unchanged and only adds wrapper files around it.

## Files Added

- `run_email_alert.bat`: launches `main.py` from the existing virtual environment without keeping a terminal open.
- `service.py`: Windows Service wrapper using `pywin32`; it starts `main.py` as a child process and restarts it if it exits unexpectedly.
- `install_service.bat`: installs and starts the Windows Service.

## 1. One-Time Preparation

Open PowerShell in the project folder:

```powershell
cd "C:\Users\magli\Desktop\Smart Email-Alert-System"
```

If dependencies are not installed yet:

```powershell
.\venv\Scripts\pip.exe install -r requirements.txt
.\venv\Scripts\pip.exe install pywin32
```

If `pywin32` was just installed, run:

```powershell
.\venv\Scripts\pywin32_postinstall.exe -install
```

## 2. Approach A: Task Scheduler

Use this when you want the app to start at login or at boot without showing a terminal window.

### Manual Setup Steps

1. Press `Win + R`, type `taskschd.msc`, and open Task Scheduler.
2. Click `Create Task`.
3. In `General`:
   - Name: `Smart Email Alert System`
   - Check `Run whether user is logged on or not`
   - Check `Run with highest privileges`
4. In `Triggers`:
   - Add `At log on` for your user, or `At startup` for the machine
5. In `Actions`:
   - Action: `Start a program`
   - Program/script: `C:\Users\magli\Desktop\Smart Email-Alert-System\run_email_alert.bat`
   - Start in: `C:\Users\magli\Desktop\Smart Email-Alert-System`
6. In `Conditions`:
   - Uncheck `Start the task only if the computer is on AC power` if needed
7. In `Settings`:
   - Check `Run task as soon as possible after a scheduled start is missed`
   - Check `If the task fails, restart every` and choose a retry interval
8. Click `OK` and enter your Windows password if prompted.

### Command-Line Alternative

Run PowerShell as your user:

```powershell
schtasks /create /tn "Smart Email Alert System" /tr "\"C:\Users\magli\Desktop\Smart Email-Alert-System\run_email_alert.bat\"" /sc onlogon /rl highest /f
```

To start it immediately:

```powershell
schtasks /run /tn "Smart Email Alert System"
```

To remove it later:

```powershell
schtasks /delete /tn "Smart Email Alert System" /f
```

## 3. Approach B: Windows Service with `pywin32`

Use this when you want the app managed like a real background service by Windows.

### Important Note

Windows Services often run under `LocalSystem`, which may not have access to your Gmail/OAuth user profile the same way your own account does. For projects that depend on user-scoped tokens, running the service under your Windows user account is usually the safer choice.

### Service Install Steps

Open PowerShell as `Administrator`:

```powershell
cd "C:\Users\magli\Desktop\Smart Email-Alert-System"
.\install_service.bat
```

Or run the commands directly:

```powershell
.\venv\Scripts\python.exe .\service.py install
.\venv\Scripts\python.exe .\service.py start
```

### Service Management Commands

Start:

```powershell
.\venv\Scripts\python.exe .\service.py start
```

Stop:

```powershell
.\venv\Scripts\python.exe .\service.py stop
```

Restart:

```powershell
.\venv\Scripts\python.exe .\service.py restart
```

Remove:

```powershell
.\venv\Scripts\python.exe .\service.py stop
.\venv\Scripts\python.exe .\service.py remove
```

### Set Service Logon Account

After installing:

1. Press `Win + R`
2. Run `services.msc`
3. Open `Smart Email Alert System`
4. Go to `Log On`
5. Select `This account`
6. Enter your Windows username and password
7. Apply, then restart the service

## 4. Logs and Verification

Both approaches write logs here:

```text
C:\Users\magli\Desktop\Smart Email-Alert-System\logs\
```

Main places to check:

- `logs\email_alert.log`: output from the Task Scheduler launcher
- `logs\service.log`: service wrapper lifecycle and child process status

Quick manual test:

```powershell
.\run_email_alert.bat
```

Then verify the process is running:

```powershell
Get-Process python, pythonw -ErrorAction SilentlyContinue
```

## 5. Which Option to Choose

- Choose `Task Scheduler` if you want the simplest setup and your app relies on your normal signed-in user context.
- Choose `Windows Service` if you want Windows-native service management, restart control, and startup before user login.
