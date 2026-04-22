from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import servicemanager
import win32event
import win32service
import win32serviceutil


BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "service.log"
MAIN_SCRIPT = BASE_DIR / "main.py"
PYTHON_EXE = BASE_DIR / "venv" / "Scripts" / "python.exe"


class SmartEmailAlertService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SmartEmailAlertService"
    _svc_display_name_ = "Smart Email Alert System"
    _svc_description_ = "Runs the Smart Email Alert System in the background on Windows."

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.process: subprocess.Popen | None = None
        self.log_handle = None
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        self._stop_child_process()
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        servicemanager.LogInfoMsg(f"{self._svc_name_} is starting.")
        self._run_service()

    def _run_service(self):
        while self.running:
            try:
                self._start_child_process()
                self._wait_for_child_process()
            except Exception as exc:  # pragma: no cover - Windows service path
                self._write_log(f"Service error: {exc}")
                time.sleep(5)

    def _start_child_process(self):
        if not PYTHON_EXE.exists():
            raise FileNotFoundError(f"Virtual environment Python not found: {PYTHON_EXE}")
        if not MAIN_SCRIPT.exists():
            raise FileNotFoundError(f"main.py not found: {MAIN_SCRIPT}")

        LOG_DIR.mkdir(exist_ok=True)
        self.log_handle = open(LOG_FILE, "a", encoding="utf-8")

        self.process = subprocess.Popen(
            [str(PYTHON_EXE), str(MAIN_SCRIPT)],
            cwd=str(BASE_DIR),
            stdout=self.log_handle,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        self._write_log(f"Started child process with PID {self.process.pid}")

    def _wait_for_child_process(self):
        if self.process is None:
            return

        while self.running:
            exit_code = self.process.poll()
            if exit_code is not None:
                self._write_log(f"Child process exited with code {exit_code}. Restarting in 5 seconds.")
                if self.log_handle is not None:
                    self.log_handle.close()
                    self.log_handle = None
                self.process = None
                time.sleep(5)
                return

            wait_result = win32event.WaitForSingleObject(self.stop_event, 1000)
            if wait_result == win32event.WAIT_OBJECT_0:
                return

    def _stop_child_process(self):
        if self.process is None:
            return

        self._write_log("Stopping child process.")
        self.process.terminate()

        try:
            self.process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            self._write_log("Child process did not stop in time. Killing it.")
            self.process.kill()
            self.process.wait(timeout=5)
        finally:
            if self.log_handle is not None:
                self.log_handle.close()
                self.log_handle = None
            self.process = None

    def _write_log(self, message: str):
        LOG_DIR.mkdir(exist_ok=True)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(f"[{timestamp}] {message}\n")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(SmartEmailAlertService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(SmartEmailAlertService)
