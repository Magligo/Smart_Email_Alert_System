import time

from email_reader import EmailReader
from meeting_detector import MeetingDetector
from notifier import Notifier
from parser import EmailParser
from priority_classifier import PriorityClassifier
from scheduler import MeetingScheduler


def main():
    reader = EmailReader()
    parser = EmailParser()
    detector = MeetingDetector()
    classifier = PriorityClassifier()
    scheduler = MeetingScheduler()
    notifier = Notifier()

    processed_emails = set()  # Avoid duplicate processing while polling.

    try:
        while True:
            raw_emails = reader.fetch_emails()
            parsed_emails = [parser.parse(email) for email in raw_emails]

            for email in parsed_emails:
                email_id = email.subject + email.sender

                if email_id in processed_emails:
                    continue

                processed_emails.add(email_id)

                meeting = detector.detect(email)
                if not meeting:
                    continue

                priority = classifier.classify(email, meeting)

                # The scheduler is the single place that decides whether to:
                # 1. skip finished meetings
                # 2. notify immediately for still-upcoming meetings
                # 3. schedule a reminder before the meeting
                scheduler.schedule(
                    meeting,
                    priority,
                    notifier.notify,
                    email,
                )

            time.sleep(30)

    except KeyboardInterrupt:
        print("\nSystem stopped gracefully")


if __name__ == "__main__":
    main()
