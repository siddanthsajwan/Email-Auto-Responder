from crewai.tools import tool
from email_auto_responder_flow.utils.imap_utils import get_thread as imap_get_thread

class GetThreadTool:
    @tool("Get Email Thread")
    def get_thread(thread_id: str) -> str:
        """
        Useful to get the entire context and history of an email thread.
        The input should be the threadId of the email.
        """
        try:
            thread_text = imap_get_thread(thread_id)
            if not thread_text:
                return "Thread not found or empty."
            return thread_text
        except Exception as e:
            return f"Error retrieving thread: {e}"
