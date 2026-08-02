import os
import time
from typing import List

from email_auto_responder_flow.types import Email
from email_auto_responder_flow.utils.imap_utils import fetch_recent_emails


AUTOMATED_PATTERNS = [
    "donotreply@",
    "no-reply@",
    "noreply@",
    "jobalert@",
    "alertnc@",
    "mailer@",
    "newsletter@",
    "notification@",
    "notifications@",
    "promo@",
    "promotions@",
    "transactions@",
]


def check_email(checked_emails_ids: set[str]) -> tuple[list[Email], set[str]]:
    print("# Checking for new emails")

    emails = fetch_recent_emails(days_ago=1, max_emails=10)
    thread = []
    new_emails: List[Email] = []
    for email in emails:
        sender_lower = email["sender"].lower()
        is_automated = any(pattern in sender_lower for pattern in AUTOMATED_PATTERNS)
        
        if (
            (email["id"] not in checked_emails_ids)
            and (email["threadId"] not in thread)
            and (os.environ.get("MY_EMAIL", "").lower() not in sender_lower)
            and not is_automated
        ):
            thread.append(email["threadId"])
            new_emails.append(
                Email(
                    id=email["id"],
                    threadId=email["threadId"],
                    snippet=email["snippet"],
                    sender=email["sender"],
                )
            )
    checked_emails_ids.update([email["id"] for email in emails])
    return new_emails, checked_emails_ids


def wait_next_run(state):
    print("## Waiting for 180 seconds")
    time.sleep(180)
    return state


def new_emails(state):
    if len(state["emails"]) == 0:
        print("## No new emails")
        return "end"
    else:
        print("## New emails")
        return "continue"


def format_emails(emails):
    emails_string = []
    for email in emails:
        email_id = email.id if hasattr(email, 'id') else email['id']
        email_threadId = email.threadId if hasattr(email, 'threadId') else email['threadId']
        email_snippet = email.snippet if hasattr(email, 'snippet') else email['snippet']
        email_sender = email.sender if hasattr(email, 'sender') else email['sender']
        
        arr = [
            f"ID: {email_id}",
            f"- Thread ID: {email_threadId}",
            f"- Snippet: {email_snippet}",
            f"- From: {email_sender}",
            "--------",
        ]
        emails_string.append("\n".join(arr))
    return "\n".join(emails_string)
