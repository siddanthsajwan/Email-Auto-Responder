import email
import imaplib
import os
import time
from datetime import datetime, timedelta
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def get_imap_client():
    """Establish and return an IMAP connection."""
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    email_address = os.environ.get("MY_EMAIL")
    password = os.environ.get("EMAIL_PASSWORD")
    
    if not email_address or not password:
        raise ValueError("MY_EMAIL and EMAIL_PASSWORD must be set in the environment.")
    
    mail.login(email_address, password)
    return mail

def get_text_from_email(msg):
    """Extract text content from an email message object."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    return part.get_payload(decode=True).decode()
                except:
                    return part.get_payload()
    else:
        try:
            return msg.get_payload(decode=True).decode()
        except:
            return msg.get_payload()
    return ""

def fetch_recent_emails(days_ago=1, max_emails=10):
    """Fetch emails from the last `days_ago` days, up to `max_emails`."""
    mail = get_imap_client()
    mail.select("inbox")
    
    date = (datetime.now() - timedelta(days=days_ago)).strftime("%d-%b-%Y")
    status, messages = mail.search(None, f'(SINCE "{date}")')
    
    email_data = []
    
    if status == "OK" and messages[0]:
        email_ids = messages[0].split()
        for i, e_id in enumerate(reversed(email_ids)): # Process newest first
            if i >= max_emails: # Limit batch size for token efficiency
                break
            
            # Fetch message data and thread ID using UID and X-GM-THRID (Gmail specific)
            status, msg_data = mail.fetch(e_id, "(RFC822 X-GM-THRID)")
            if status == "OK":
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Extract thread ID from the response part (e.g., b'1 (X-GM-THRID 1709429490218987411 RFC822 {724}')
                        meta_info = response_part[0].decode(errors="ignore")
                        thread_id = "unknown"
                        if "X-GM-THRID" in meta_info:
                            try:
                                thread_id = meta_info.split("X-GM-THRID ")[1].split(" ")[0]
                            except Exception:
                                pass
                        
                        body = get_text_from_email(msg)
                        snippet = body[:200].replace('\n', ' ') if body else ""
                        
                        email_data.append({
                            "id": e_id.decode(),
                            "threadId": thread_id,
                            "snippet": snippet,
                            "sender": msg.get("From", ""),
                        })
    mail.logout()
    # Return chronologically ascending order if needed, but reversing is fine for flow processing
    return email_data

def get_thread(thread_id: str):
    """Fetch all emails belonging to a specific Gmail thread ID."""
    if not thread_id or not str(thread_id).strip().isdigit():
        return "Invalid thread ID. Thread ID must be a valid numeric ID."

    mail = get_imap_client()
    mail.select("inbox")
    
    # Use Gmail's specific search syntax for thread ID
    status, messages = mail.uid('search', None, f'X-GM-THRID {thread_id}')
    
    thread_text = ""
    
    if status == "OK" and messages[0]:
        email_ids = messages[0].split()
        for i, uid in enumerate(email_ids):
            status, msg_data = mail.uid('fetch', uid, '(RFC822)')
            if status == "OK":
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        sender = msg.get("From", "")
                        date = msg.get("Date", "")
                        subject = msg.get("Subject", "")
                        body = get_text_from_email(msg)
                        
                        thread_text += f"From: {sender}\nDate: {date}\nSubject: {subject}\n\n{body}\n\n{'='*40}\n\n"
                        
    mail.logout()
    return thread_text

def create_draft(to_email: str, subject: str, message_body: str) -> bool:
    """Create an email and append it to the Gmail Drafts folder."""
    mail = get_imap_client()
    
    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.environ.get("MY_EMAIL")
    msg['To'] = to_email
    msg.set_content(message_body)
    
    success = False
    draft_folders = ['"[Gmail]/Drafts"', '[Gmail]/Drafts', '"[Google Mail]/Drafts"', '[Google Mail]/Drafts', '"Drafts"', 'Drafts']
    
    for folder in draft_folders:
        try:
            res, _ = mail.append(folder, '', imaplib.Time2Internaldate(time.time()), msg.as_bytes())
            if res == "OK":
                success = True
                break
        except Exception:
            continue
            
    if not success:
        for folder in draft_folders:
            try:
                res, _ = mail.append(folder, None, imaplib.Time2Internaldate(time.time()), msg.as_bytes())
                if res == "OK":
                    success = True
                    break
            except Exception:
                continue

    mail.logout()
    return success
