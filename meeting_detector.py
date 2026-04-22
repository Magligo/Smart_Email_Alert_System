import re
from dataclasses import dataclass
from typing import Optional

from parser import ParsedEmail


@dataclass
class MeetingDetails:
    title: str
    date_reference: str
    time_reference: str
    location: str
    relative_time_value: Optional[int] = None
    relative_time_unit: Optional[str] = None
    pattern_type: str = "absolute"


class MeetingDetector:
    """Detects whether an email contains meeting-related information."""

    MEETING_KEYWORDS = ("meeting", "sync", "call", "demo", "standup")
    DATE_PATTERN = (
        r"\b(today|tomorrow|monday|tuesday|wednesday|thursday|friday|"
        r"saturday|sunday)\b"
    )
    NEXT_WEEKDAY_PATTERN = (
        r"\bnext\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b"
    )
    TIME_OF_DAY_PATTERN = r"\bthis\s+(morning|afternoon|evening)\b"
    RELATIVE_TIME_PATTERN = r"\bin\s+(\d+)\s+(hour|hours|minute|minutes)\b"
    TIME_PATTERN = r"\b\d{1,2}(?::\d{2})?\s?(?:AM|PM|am|pm)\b"

    def detect(self, email: ParsedEmail) -> Optional[MeetingDetails]:
        text = email.combined_text.lower()

        if not any(keyword in text for keyword in self.MEETING_KEYWORDS):
            return None

        relative_time = self._extract_relative_time(text)
        if relative_time:
            value, unit = relative_time
            print("Detected pattern type: relative_time")
            return MeetingDetails(
                title=email.subject,
                date_reference="relative",
                time_reference="relative",
                location=self._extract_location(text),
                relative_time_value=value,
                relative_time_unit=unit,
                pattern_type="relative_time",
            )

        next_weekday = self._extract_next_weekday(text)
        if next_weekday:
            time_reference = (
                self._extract_first_match(email.combined_text, (self.TIME_PATTERN,))
                or "unspecified"
            )
            print("Detected pattern type: next_weekday")
            return MeetingDetails(
                title=email.subject,
                date_reference=next_weekday,
                time_reference=time_reference,
                location=self._extract_location(text),
                pattern_type="next_weekday",
            )

        time_of_day = self._extract_time_of_day(text)
        if time_of_day:
            date_reference = self._extract_date_reference(text)
            print("Detected pattern type: time_of_day")
            return MeetingDetails(
                title=email.subject,
                date_reference=date_reference,
                time_reference=time_of_day,
                location=self._extract_location(text),
                pattern_type="time_of_day",
            )

        date_reference = self._extract_date_reference(text)
        time_reference = (
            self._extract_first_match(email.combined_text, (self.TIME_PATTERN,))
            or "unspecified"
        )
        print("Detected pattern type: absolute")
        return MeetingDetails(
            title=email.subject,
            date_reference=date_reference,
            time_reference=time_reference,
            location=self._extract_location(text),
            pattern_type="absolute",
        )

    def _extract_first_match(self, text: str, patterns: tuple[str, ...]) -> Optional[str]:
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                return match.group(0)
        return None

    def _extract_relative_time(self, text: str) -> Optional[tuple[int, str]]:
        match = re.search(self.RELATIVE_TIME_PATTERN, text, flags=re.IGNORECASE)
        if not match:
            return None

        value = int(match.group(1))
        unit = match.group(2).lower()
        normalized_unit = "hours" if "hour" in unit else "minutes"
        return value, normalized_unit

    def _extract_next_weekday(self, text: str) -> Optional[str]:
        match = re.search(self.NEXT_WEEKDAY_PATTERN, text, flags=re.IGNORECASE)
        if not match:
            return None
        return f"next {match.group(1).lower()}"

    def _extract_time_of_day(self, text: str) -> Optional[str]:
        match = re.search(self.TIME_OF_DAY_PATTERN, text, flags=re.IGNORECASE)
        if not match:
            return None
        return f"this {match.group(1).lower()}"

    def _extract_location(self, text: str) -> str:
        return "conference room" if "conference room" in text else "to be confirmed"

    def _extract_date_reference(self, text: str) -> str:
        """Return a normalized lowercase date label.

        Missing dates fall back to "today" so the scheduler can still build a
        complete datetime from time-only meeting emails.
        """
        match = re.search(self.DATE_PATTERN, text, flags=re.IGNORECASE)
        if not match:
            return "today"
        return match.group(0).lower()
