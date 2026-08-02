# 📧 Email Auto Responder Flow

An intelligent, multi-agent AI email assistant built with **[crewAI Flows](https://crewai.com)** and **Groq (Llama 3.1)**. It automatically scans your Gmail inbox, filters out spam and automated emails, analyzes conversation context for emails requiring action, and crafts tailored draft responses directly into your **Gmail Drafts** folder.

---

## 🏗️ Architecture & How It Works

```
                     ┌───────────────────────┐
                     │   Gmail Inbox (IMAP)  │
                     └──────────┬────────────┘
                                │ Fetches recent emails
                                ▼
                   ┌───────────────────────────┐
                   │   Email Filtering Agent   │  Filters out newsletters, spam,
                   │  (Senior Email Analyst)   │  promotions, and automated alerts
                   └────────────┬──────────────┘
                                │ Identifies actionable emails
                                ▼
                   ┌───────────────────────────┐
                   │    Email Action Agent     │  Uses 'Get Email Thread' tool
                   │ (Email Action Specialist) │  to fetch full thread history
                   └────────────┬──────────────┘
                                │ Context & action points
                                ▼
                   ┌───────────────────────────┐
                   │   Email Response Writer   │  Drafts contextual responses and saves
                   │  (Email Response Writer)  │  to Gmail via 'Create Draft' tool
                   └────────────┬──────────────┘
                                │
                                ▼
                     ┌───────────────────────┐
                     │  Gmail Drafts Folder  │  Ready for your final review & send!
                     └───────────────────────┘
```

---

## ⚙️ Prerequisites & Setup

### 1. Gmail IMAP & App Password Setup
1. **Enable IMAP in Gmail**:
   - Go to **Gmail Settings** (gear icon) ➔ **See all settings** ➔ **Forwarding and POP/IMAP**.
   - Under *IMAP access*, select **Enable IMAP** and click **Save Changes**.
2. **Generate a Gmail App Password**:
   - Go to your [Google Account Security](https://myaccount.google.com/security).
   - Ensure **2-Step Verification** is turned ON.
   - Search for **App passwords** (or go to `Security` ➔ `2-Step Verification` ➔ `App passwords`).
   - Create a new App Password named `CrewAI Email Responder`.
   - Copy the 16-character generated password (e.g., `abcd efgh ijkl mnop`).

### 2. Environment Variables (`.env`)
Create or edit the `.env` file in the project folder (`crewAI-examples/flows/email_auto_responder_flow/.env`):

```env
# LLM Configuration (Groq - Free & High Performance)
GROQ_API_KEY=gsk_your_groq_api_key_here
MODEL=groq/llama-3.1-8b-instant

# Search API Keys
SERPER_API_KEY=your_serper_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# Gmail Configuration
MY_EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password
```

---

## 🚀 Running the Project

### Option 1: Navigate to the Project Directory (Recommended)
Open PowerShell or your terminal and run:

```powershell
cd "D:\email auto responder\crewAI-examples\flows\email_auto_responder_flow"
uv run kickoff
```

### Option 2: Run directly from Workspace Root
If your terminal is in the root directory (`D:\email auto responder`):

```powershell
uv --directory "crewAI-examples\flows\email_auto_responder_flow" run kickoff
```

### Option 3: Run directly with Python
```powershell
cd "D:\email auto responder\crewAI-examples\flows\email_auto_responder_flow"
& ".\.venv\Scripts\python.exe" -m email_auto_responder_flow.main
```

---

## 🛠️ Agents & Tools Breakdown

| Agent / Component | Role | Tools Used | Description |
| :--- | :--- | :--- | :--- |
| **EmailFilterCrew** | Orchestrator | — | Sequential process executing the 3 agents. |
| **email_filter_agent** | Senior Email Analyst | — | Analyzes inbox batch and filters out noise and automated notifications. |
| **email_action_agent** | Email Action Specialist | `Get Email Thread` | Uses Gmail thread ID to pull full conversation context. |
| **email_response_writer** | Email Response Writer | `Create Draft` | Drafts a professional reply and appends it to `[Gmail]/Drafts`. |

---

## ⚡ Built-in Rate Limit & Stability Features

- **Groq TPM Guard**: Automatic exponential retry & 15-second pauses if Groq's Free-tier Tokens-Per-Minute limit is reached.
- **Inter-Task Pauses**: 10-second buffer between crew tasks to prevent burst quota exhaustion.
- **Resilient Draft Resolution**: Automatically resolves draft folders across Gmail aliases (`[Gmail]/Drafts`, `[Google Mail]/Drafts`, `Drafts`).
- **Pydantic Tool Input Schemas**: Supports flexible structured inputs and keyword variations from LLM function calls.
