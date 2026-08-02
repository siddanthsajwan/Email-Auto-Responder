from typing import Optional
from crewai.tools import tool
from email_auto_responder_flow.utils.imap_utils import create_draft as imap_create_draft


class CreateDraftTool:
    @tool("Create Draft")
    def create_draft(
        to_email: Optional[str] = None,
        subject: str = "",
        message: Optional[str] = None,
        to: Optional[str] = None,
        body: Optional[str] = None,
        message_body: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Useful to create an email draft in Gmail.
        Parameters:
        - to_email: Recipient email address
        - subject: Subject line of the email draft
        - message: The drafted email message body
        """
        recipient = to_email or to or kwargs.get("email") or kwargs.get("recipient")
        content = message or message_body or body or kwargs.get("content") or kwargs.get("text")

        # Support raw pipe-separated format if passed as a string or in 'data'
        if not recipient and "data" in kwargs:
            data = kwargs["data"]
            if isinstance(data, dict):
                recipient = data.get("to") or data.get("email") or data.get("to_email")
                subject = data.get("subject", subject)
                content = data.get("message") or data.get("body")
            elif isinstance(data, str) and "|" in data:
                parts = data.split("|", 2)
                recipient = parts[0].strip()
                subject = parts[1].strip() if len(parts) > 1 else subject
                content = parts[2].strip() if len(parts) > 2 else ""

        if not recipient:
            return "Error: Missing recipient email address."
        if not content:
            return "Error: Missing draft message body."

        try:
            success = imap_create_draft(
                to_email=str(recipient).strip(),
                subject=str(subject).strip(),
                message_body=str(content).strip(),
            )
            if success:
                return f"\nDraft created successfully for {recipient} with subject '{subject}'.\n"
            else:
                return f"\nFailed to save draft to Gmail Drafts folder for {recipient}.\n"
        except Exception as e:
            return f"\nError creating draft: {e}\n"
