from plyer import notification


class Notifier:
    """Shows system notification."""

    def notify(self, email, meeting, priority, scheduled_time):
        message = (
            f"{priority.upper()} Meeting\n"
            f"Time: {meeting.time_reference}\n"
            f"From: {email.sender}\n"
            f"Purpose: {meeting.title}"
        )

        print("NOTIFICATION:", message)

        notification.notify(
            title="Meeting Alert",
            message=message,
            timeout=10
        )