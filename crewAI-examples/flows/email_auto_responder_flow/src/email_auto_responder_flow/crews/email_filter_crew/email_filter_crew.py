import os
import time
import litellm
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import TavilySearchTool
from email_auto_responder_flow.tools.get_thread import GetThreadTool
from crewai import LLM

from email_auto_responder_flow.tools.create_draft import CreateDraftTool

# Configure litellm for robust retry and rate-limit recovery
_original_litellm_completion = litellm.completion

def safe_rate_limit_completion(*args, **kwargs):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            return _original_litellm_completion(*args, **kwargs)
        except litellm.exceptions.RateLimitError as e:
            if attempt < max_retries - 1:
                print(f"\n[Rate Limit] Groq TPM limit reached. Pausing 15s for quota reset (Retry {attempt + 1}/{max_retries})...")
                time.sleep(15)
            else:
                raise e

litellm.completion = safe_rate_limit_completion


def rate_limit_pause(task_output):
    """Pause between tasks to prevent bursting past Groq free-tier TPM limits."""
    time.sleep(10)


@CrewBase
class EmailFilterCrew:
    """Email Filter Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = LLM(
        model=os.environ.get("MODEL", "groq/llama-3.1-8b-instant"),
        num_retries=6,
    )

    @agent
    def email_filter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["email_filter_agent"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def email_action_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["email_action_agent"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            tools=[
                GetThreadTool.get_thread,
            ],
        )

    @agent
    def email_response_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["email_response_writer"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            tools=[
                CreateDraftTool.create_draft,
            ],
        )

    @task
    def filter_emails_task(self) -> Task:
        return Task(config=self.tasks_config["filter_emails"], callback=rate_limit_pause)

    @task
    def action_required_emails_task(self) -> Task:
        return Task(config=self.tasks_config["action_required_emails"], callback=rate_limit_pause)

    @task
    def draft_responses_task(self) -> Task:
        return Task(config=self.tasks_config["draft_responses"])

    @crew
    def crew(self) -> Crew:
        """Creates the Email Filter Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
