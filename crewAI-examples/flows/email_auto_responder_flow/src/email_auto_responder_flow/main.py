#!/usr/bin/env python
import os
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import List

from dotenv import load_dotenv

load_dotenv()

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from email_auto_responder_flow.types import Email
from email_auto_responder_flow.utils.emails import check_email, format_emails

from .crews.email_filter_crew.email_filter_crew import EmailFilterCrew


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Email Auto Responder - Live Status</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * { box-sizing: border-box; margin: 0; padding: 0; }
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                    background: #0f172a;
                    color: #f8fafc;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    padding: 1.5rem;
                }
                .card {
                    background: #1e293b;
                    padding: 2.5rem;
                    border-radius: 1.25rem;
                    box-shadow: 0 20px 35px rgba(0,0,0,0.4);
                    border: 1px solid #334155;
                    max-width: 480px;
                    width: 100%;
                    text-align: center;
                }
                .status-badge {
                    display: inline-flex;
                    align-items: center;
                    gap: 0.6rem;
                    background: rgba(16, 185, 129, 0.15);
                    color: #34d399;
                    padding: 0.45rem 1.1rem;
                    border-radius: 9999px;
                    font-weight: 600;
                    font-size: 0.875rem;
                    margin-bottom: 1.5rem;
                    border: 1px solid rgba(52, 211, 153, 0.3);
                }
                .pulse {
                    width: 10px;
                    height: 10px;
                    background: #34d399;
                    border-radius: 50%;
                    box-shadow: 0 0 0 0 rgba(52, 211, 153, 1);
                    animation: pulse 2s infinite;
                }
                @keyframes pulse {
                    0% { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7); }
                    70% { box-shadow: 0 0 0 10px rgba(52, 211, 153, 0); }
                    100% { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0); }
                }
                h1 { font-size: 1.6rem; margin-bottom: 0.6rem; font-weight: 700; }
                p { color: #94a3b8; font-size: 0.95rem; line-height: 1.6; }
                .info-box {
                    background: #0f172a;
                    border-radius: 0.75rem;
                    padding: 1.2rem;
                    margin-top: 1.75rem;
                    text-align: left;
                    font-size: 0.875rem;
                    border: 1px solid #1e293b;
                }
                .info-row {
                    display: flex;
                    justify-content: space-between;
                    padding: 0.45rem 0;
                    border-bottom: 1px solid #1e293b;
                }
                .info-row:last-child { border-bottom: none; }
                .info-row span { color: #64748b; }
                .info-row strong { color: #e2e8f0; }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="status-badge"><div class="pulse"></div> Live & Actively Monitoring</div>
                <h1>📧 Email Auto Responder</h1>
                <p>Autonomous AI Multi-Agent Flow monitoring Gmail inbox and drafting contextual replies.</p>
                <div class="info-box">
                    <div class="info-row"><span>Framework:</span><strong>CrewAI Flows</strong></div>
                    <div class="info-row"><span>Model:</span><strong>Groq (Llama 3.1 8B)</strong></div>
                    <div class="info-row"><span>Email Worker:</span><strong style="color: #34d399;">Active (IMAP)</strong></div>
                    <div class="info-row"><span>Action:</span><strong>Auto-Draft to Gmail</strong></div>
                </div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

    def log_message(self, format, *args):
        return


def start_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Health check dashboard listening on port {port}")
    server.serve_forever()


class AutoResponderState(BaseModel):
    id: str = "email_auto_responder_flow"
    emails: List[Email] = []
    checked_emails_ids: set[str] = set()


class EmailAutoResponderFlow(Flow[AutoResponderState]):
    initial_state = AutoResponderState

    @start()
    def fetch_new_emails(self):
        print("Kickoff the Email Filter Crew")
        new_emails, updated_checked_email_ids = check_email(
            checked_emails_ids=self.state.checked_emails_ids
        )

        self.state.emails = new_emails
        self.state.checked_emails_ids = updated_checked_email_ids

    @listen(fetch_new_emails)
    def generate_draft_responses(self):
        print("Current email queue: ", len(self.state.emails))
        if len(self.state.emails) > 0:
            print("Writing New emails")
            emails = format_emails(self.state.emails)

            EmailFilterCrew().crew().kickoff(inputs={"emails": emails})

            self.state.emails = []


def kickoff():
    """
    Run the flow and keep the health server active.
    """
    # Start web dashboard in daemon thread for Render web service compatibility
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()

    print("Starting continuous Email Auto Responder Flow loop...")
    shared_checked_ids = set()
    while True:
        try:
            flow = EmailAutoResponderFlow()
            flow.state.checked_emails_ids = shared_checked_ids
            flow.kickoff()
            shared_checked_ids = flow.state.checked_emails_ids
        except Exception as e:
            print(f"Error in flow execution: {e}")

        print("Waiting 180 seconds before next inbox scan...")
        time.sleep(180)


def plot_flow():
    """
    Plot the flow.
    """
    email_auto_response_flow = EmailAutoResponderFlow()
    email_auto_response_flow.plot()


if __name__ == "__main__":
    kickoff()

