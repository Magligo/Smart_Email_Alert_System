# Smart Email Meeting Alert System

## Overview

Smart Email Meeting Alert System is a Python-based automation project that reads emails from Gmail, detects meeting-related content, extracts date and time information, and sends desktop notifications for upcoming meetings.

The system combines Gmail API integration, regex-based parsing, and rule-based natural language handling to understand both explicit and human-friendly meeting phrases such as `tomorrow`, `next Friday`, `this evening`, and `in 2 hours`. It is designed to run continuously in the background and help users avoid missing important meetings buried in email threads.

## Features

- Gmail API integration with OAuth 2.0 authentication
- Reads and processes incoming emails from Gmail
- Parses email content into structured data
- Detects meeting-related messages using regex and NLP-style rules
- Extracts time formats such as `6 PM` and `6:30pm`
- Understands natural language expressions such as:
  - `today`
  - `tomorrow`
  - weekdays like `Monday` to `Sunday`
  - `next Friday`
  - `this evening`
  - `in 2 hours`
- Smart scheduling logic for reminders
- Skips past meetings automatically
- Sends alerts only for upcoming meetings
- Triggers immediate notification when a meeting is very close
- Prevents duplicate notifications for the same meeting
- Supports background execution on Windows using Task Scheduler
- Includes logging support for monitoring and debugging

## Tech Stack

- Python
- Gmail API
- OAuth 2.0
- Regex
- Rule-based NLP logic
- `datetime`
- `threading`
- Plyer

## Project Structure

```text
Smart Email-Alert-System/
|
|-- main.py                  # Main entry point for continuous email monitoring
|-- email_reader.py          # Gmail API integration and email fetching
|-- parser.py                # Email parsing and structured extraction
|-- meeting_detector.py      # Meeting detection using regex and language rules
|-- scheduler.py             # Reminder scheduling logic
|-- notifier.py              # Desktop notification handling
|-- priority_classifier.py   # Priority classification for detected meetings
|-- credentials.json         # Gmail API OAuth client credentials
|-- token.json               # Stored OAuth access token
|-- requirements.txt         # Python dependencies
|-- run_email_alert.bat      # Background launcher for Windows
|-- install_service.bat      # Optional service install helper
|-- WINDOWS_SETUP.md         # Windows background execution guide
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Smart Email-Alert-System
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install plyer
```

### 4. Set Up Gmail API Access

1. Open Google Cloud Console
2. Create a project or select an existing one
3. Enable the Gmail API
4. Create OAuth 2.0 credentials
5. Download the credentials file
6. Save it in the project root as `credentials.json`

### 5. Authenticate the Application

Run the project once to complete OAuth authorization and generate `token.json`.

```bash
python main.py
```

### 6. Run the Application

```bash
python main.py
```

### 7. Run in Background on Windows

To run the system without opening a terminal each time, use the provided batch launcher with Windows Task Scheduler.

```bash
run_email_alert.bat
```

For scheduled startup, follow the steps in `WINDOWS_SETUP.md`.

## How It Works

1. The system connects to Gmail using the Gmail API.
2. It fetches email messages at regular intervals.
3. Each email is parsed into a structured format.
4. The detector checks whether the email contains meeting-related content.
5. Date and time information is extracted using regex and rule-based logic.
6. Natural language time expressions are converted into actual upcoming datetimes.
7. The scheduler decides whether to:
   - ignore past meetings
   - notify immediately
   - schedule a reminder shortly before the meeting
8. Duplicate alerts are avoided using internal tracking.

## Example Use Cases

- Receive a desktop alert when an email says: `Meeting tomorrow at 6 PM`
- Detect a reminder from a message like: `Let's connect next Friday evening`
- Trigger an immediate alert for: `Call in 2 hours`
- Ignore old meeting emails for events that already passed
- Run continuously in the background to monitor work emails automatically

## Future Improvements

- Support Outlook and IMAP in addition to Gmail
- Add calendar integration for automatic event creation
- Improve NLP with ML-based intent detection
- Store processed meetings in a database
- Add a web dashboard for monitoring alerts and logs
- Support email summarization and smart priority ranking
- Add cross-platform background execution support

## Resume-Ready Highlights

- Built a Python automation system for Gmail-based meeting detection and alerting
- Implemented regex and rule-based NLP for natural language time understanding
- Integrated OAuth 2.0 and Gmail API for secure email access
- Designed smart scheduling logic with duplicate prevention and upcoming-event filtering
- Enabled background execution on Windows for real-world usability
