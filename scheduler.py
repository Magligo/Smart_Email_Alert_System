from datetime import datetime, timedelta
import re
import threading


class MeetingScheduler:
    def __init__(self):
        self.scheduled_meetings = set()

        self.days_map = {
            "monday": 0, "tuesday": 1, "wednesday": 2,
            "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6,
        }

        self.time_of_day_defaults = {
            "this morning": "9 AM",
            "this afternoon": "2 PM",
            "this evening": "6 PM",
        }

    def schedule(self, meeting, priority, callback, email):
        now = datetime.now()

        meeting_datetime = self._resolve_meeting_datetime(meeting, now)
        if meeting_datetime is None:
            return

        # ❌ Skip past meetings
        if meeting_datetime <= now:
            print("❌ Skipping: meeting already finished")
            return

        print(f"📅 Meeting datetime: {meeting_datetime}")
        print(f"⏱ Current time: {now}")

        # ✅ Avoid duplicate scheduling
        meeting_key = (
            getattr(email, "sender", ""),
            getattr(meeting, "title", ""),
            meeting_datetime.isoformat(),
        )

        if meeting_key in self.scheduled_meetings:
            print("⚠️ Duplicate meeting skipped")
            return

        self.scheduled_meetings.add(meeting_key)

        # ✅ Smart immediate notification (only if near)
        time_diff = (meeting_datetime - now).total_seconds()

        if time_diff <= 300:  # 5 minutes
            print("⚡ Meeting soon → notifying now")
            callback(email, meeting, priority, "NOW")

        # ✅ Reminder logic
        if priority == "urgent":
            notify_time = meeting_datetime - timedelta(minutes=1)
        else:
            notify_time = meeting_datetime - timedelta(minutes=5)

        delay = (notify_time - now).total_seconds()

        if delay > 0:
            print(f"⏳ Scheduled reminder at {notify_time}")

            threading.Timer(
                delay,
                callback,
                args=[email, meeting, priority, notify_time]
            ).start()

        else:
            print("⚡ Reminder time passed but meeting upcoming → notify now")
            callback(email, meeting, priority, "NOW")

    # =============================

    def _resolve_meeting_datetime(self, meeting, now):
        pattern_type = getattr(meeting, "pattern_type", "absolute")
        print(f"Detected pattern type: {pattern_type}")

        # ✅ Relative time (in 2 hours)
        if pattern_type == "relative_time":
            return self._build_relative_datetime(meeting, now)

        time_reference = getattr(meeting, "time_reference", "unspecified")

        # ❌ No time → skip
        if time_reference.lower() == "unspecified":
            print("⚠️ Skipping: no time found")
            return None

        # ✅ Handle “this evening”
        resolved_time = self.time_of_day_defaults.get(
            time_reference.lower(), time_reference
        )

        parsed_time = self._parse_time_reference(resolved_time)
        if parsed_time is None:
            print(f"❌ Unsupported time format: {time_reference}")
            return None

        return self._build_meeting_datetime(
            getattr(meeting, "date_reference", "today"),
            parsed_time,
            now
        )

    # =============================

    def _build_relative_datetime(self, meeting, now):
        value = getattr(meeting, "relative_time_value", None)
        unit = getattr(meeting, "relative_time_unit", None)

        if value is None or unit is None:
            print("❌ Missing relative time data")
            return None

        if unit == "hours":
            return now + timedelta(hours=value)

        return now + timedelta(minutes=value)

    # =============================

    def _parse_time_reference(self, time_reference):
        normalized = self._normalize_time_string(time_reference)
        print("Normalized time:", normalized)

        for fmt in ("%I:%M %p", "%I %p"):
            try:
                return datetime.strptime(normalized, fmt).time()
            except ValueError:
                continue

        return None

    # =============================

    def _normalize_time_string(self, text):
        text = text.strip()

        match = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?\s*([AaPp][Mm])", text)
        if not match:
            return text.upper()

        hour, minute, ampm = match.groups()

        if minute:
            return f"{int(hour)}:{minute} {ampm.upper()}"
        return f"{int(hour)} {ampm.upper()}"

    # =============================

    def _build_meeting_datetime(self, date_reference, time_value, now):
        date_reference = (date_reference or "today").lower()

        if date_reference == "tomorrow":
            meeting_date = now.date() + timedelta(days=1)

        elif date_reference.startswith("next "):
            day = date_reference.split(" ")[1]
            meeting_date = self._next_weekday(day, now)

        elif date_reference in self.days_map:
            target = self.days_map[date_reference]
            diff = (target - now.weekday()) % 7
            meeting_date = now.date() + timedelta(days=diff)

            # If today but time passed → next week
            candidate = datetime.combine(meeting_date, time_value)
            if candidate <= now:
                meeting_date += timedelta(days=7)

        else:
            meeting_date = now.date()

        return datetime.combine(meeting_date, time_value)

    # =============================

    def _next_weekday(self, day, now):
        target = self.days_map[day]
        diff = (target - now.weekday()) % 7

        if diff == 0:
            diff = 7

        return now.date() + timedelta(days=diff)