class PriorityClassifier:
    """Classifies meeting priority."""

    URGENT_KEYWORDS = ["urgent", "asap", "immediate", "high priority"]

    def classify(self, email, meeting) -> str:
        if not meeting:
            return "none"

        text = email.combined_text.lower()

        for word in self.URGENT_KEYWORDS:
            if word in text:
                return "urgent"

        return "normal"


# ✅ Test
if __name__ == "__main__":
    from parser import ParsedEmail

    classifier = PriorityClassifier()

    email = ParsedEmail(
        subject="Urgent Meeting",
        body="Urgent meeting at 5 PM",
        sender="boss@gmail.com",
        combined_text="Urgent Meeting Urgent meeting at 5 PM"
    )

    print(classifier.classify(email, True))