from dataclasses import dataclass


@dataclass
class ParsedEmail:
    subject: str
    body: str
    sender: str
    combined_text: str


class EmailParser:
    """Converts raw email dict into structured ParsedEmail object."""

    def parse(self, email: dict) -> ParsedEmail:
        subject = email.get("subject", "")
        body = email.get("body", "")
        sender = email.get("sender", "")

        combined_text = f"{subject} {body}"

        return ParsedEmail(
            subject=subject,
            body=body,
            sender=sender,
            combined_text=combined_text
        )


# ✅ Test
if __name__ == "__main__":
    parser = EmailParser()

    email = {
        "subject": "Meeting",
        "body": "Meeting at 2:30 PM regarding project",
        "sender": "boss@gmail.com"
    }

    parsed = parser.parse(email)
    print(parsed)