# MailSense – Intelligent Meeting Alert System

## Overview

MailSense is a Python-based alert system that reads Gmail messages, detects meeting-related content, understands human-friendly time expressions, and issues desktop notifications for upcoming meetings.

The system uses Gmail API integration with OAuth 2.0, structured email parsing, and rule-based time interpretation to identify events such as meetings, calls, and scheduling requests. MailSense is designed to filter past meetings, prioritize upcoming events, and deliver timely reminders without requiring automated setup scripts.

## Features

- Gmail API integration using OAuth 2.0
- Email parsing for meeting-related content
- Meeting detection from email body, subject, or invitation text
- Natural language time understanding for:
  - `6 PM`, `6:30 PM`
  - `today`, `tomorrow`
  - weekdays (`Monday`, `Friday`, etc.)
  - `next Friday`
  - relative expressions like `in 10 minutes`, `in 2 hours`
- Smart scheduling logic that:
  - skips meetings that have already passed
  - only triggers alerts for upcoming meetings
  - issues immediate notifications for events that are about to start
- Desktop notifications through `plyer`
- Secure credentials management with `credentials.json`

## Tech Stack

- Python
- Gmail API
- OAuth 2.0
- `requirements.txt` dependency management
- `plyer` for desktop notifications
- `datetime` for schedule calculations
- Rule-based parsing logic for natural language

## Project Structure

```text
MailSense/
|-- main.py
|-- email_reader.py
|-- parser.py
|-- meeting_detector.py
|-- scheduler.py
|-- notifier.py
|-- priority_classifier.py
|-- credentials.json       # Gmail API OAuth client credentials
|-- token.json             # Generated OAuth token after first authorization
|-- requirements.txt       # Python dependencies
|-- WINDOWS_SETUP.md       # Optional Windows guidance for background execution
```

## Installation & Setup (VERY IMPORTANT)

The project does not rely on `setup.bat` or `run.bat`. Environment setup must be completed manually.

1. Clone the repository

```bash
git clone <your-repository-url>
cd Smart_Email_Alert_System
```

2. Create a virtual environment

```bash
python -m venv venv
```

3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

5. Add `credentials.json`

- Open the Google Cloud Console
- Create or select a project
- Enable the Gmail API
- Create OAuth 2.0 client credentials
- Download the JSON credentials file
- Save the file in the project root as `credentials.json`

6. First run

```bash
python main.py
```

- The first run opens a browser for Gmail OAuth authentication
- After authorization, the app stores authentication tokens in `token.json`
- Keep `credentials.json` in the project root for future runs

## Usage

Run the project from the project folder after activating the virtual environment:

```bash
python main.py
```

## How It Works

1. MailSense connects to Gmail using the Gmail API and OAuth 2.0.
2. It fetches messages from the inbox at regular intervals.
3. Email content is parsed to extract structured text and meeting-related cues.
4. Meeting detection logic identifies event phrases and scheduling language.
5. Time expressions are converted into concrete datetimes.
6. The scheduler filters out past meetings and selects only upcoming events.
7. Notifications are generated for meetings that need attention, including immediate alerts for near-term events.

## Troubleshooting

- `ModuleNotFoundError: plyer`
  - Ensure the virtual environment is active.
  - Install dependencies with `python -m pip install -r requirements.txt`.

- Missing `credentials.json`
  - Download OAuth credentials from Google Cloud Console.
  - Place `credentials.json` in the project root.

- Notifications not showing
  - Confirm the desktop notification service is enabled on your operating system.
  - Verify `plyer` supports your Windows notification environment.

- Past meetings are skipped
  - This is intentional. MailSense only schedules alerts for upcoming events.
  - If a meeting time is already in the past, it will not generate a notification.

## Future Improvements

- Add IMAP or Outlook support in addition to Gmail
- Integrate with calendar APIs to create events automatically
- Improve natural language understanding with machine learning
- Add a lightweight web dashboard for active meeting alerts
- Persist detected meetings in a database for audit and history
- Expand cross-platform background execution support

## Summary

MailSense is a practical Python project for intelligent meeting detection from Gmail messages. It combines OAuth-secured email access, robust parsing, and smart scheduling to help users stay on top of meetings without relying on automated setup scripts.
