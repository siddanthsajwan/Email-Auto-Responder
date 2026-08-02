# Email-Auto-Responder
# CrewAI Standard Crews Examples

This directory contains examples of traditional CrewAI implementations - autonomous agent teams working together to accomplish complex tasks.

Live link - \documentclass[letterpaper,11pt]{article}
  \resumeItem{Designed a responsive Glassmorphism UI featuring dark/light modes, galleries, and PDF/JSON exports.}
\resumeItemListEnd

\resumeProjectsHeading
{{\large\textbf{Productivity Dashboard App}} $|$ \emph{React, Node.js, Express, Tailwind CSS}}{}{\href{https://task-manager-xi-ebon.vercel.app/}{\faLink} \quad \href{https://github.com/siddanthsajwan/Task-Manager}{\faGithub}}
\resumeItemListStart
  \resumeItem{Engineered frontend with optimistic updates, reducing perceived UI latency by 80\% for CRUD operations.}
  \resumeItem{Built an analytics dashboard with custom SVG charts to visualize 5+ real-time productivity metrics.}
  \resumeItem{Implemented drag-and-drop state management, improving task organization efficiency by 40\%.}
\resumeItemListEnd

\end{itemize}

%-----------SKILLS-----------
\section{Technical Skills}
\begin{itemize}[leftmargin=0.15in, label={}, itemsep=0pt, parsep=0pt, topsep=1pt]
\item {
 \textbf{Languages}: C, C++, JavaScript, HTML5, CSS3, SQL \\ \vspace{2pt}
 \textbf{Tech Stack}: React, Node.js, Express.js, MySQL, JWT, Tailwind, Tkinter, Vercel, GitHub, VS Code \\ \vspace{2pt}
 \textbf{Course Work}: Data Structure and Algorithms, OOPS, DBMS, Operating System, Computer Networks

 update the tech stack docker render and all used 
}
\end{itemize}

%-----------ACHIEVEMENTS-----------
\section{Achievements}
\resumeItemListStart
  \resumeItem{\textbf{Google Cloud Generative AI Certification} \href{https://drive.google.com/file/d/1qbtXt6xE7DhOP8Qpfkac1r-e65-lqxnB/view?usp=drivesdk}{\faLink}}
  Add my agentic AI certification by oracle here - https://drive.google.com/file/d/1B0DGq4g5sIh12M1o7iG5Nc8eDH5VQVk_/view?usp=drive_link
  \resumeItem{\textbf{Finalist, 24-Hour Hackathon conducted by the university - Graphethon}}
\resumeItemListEnd

\end{document}

## What are CrewAI Crews?

A CrewAI Crew is a team of AI agents, each with specific roles and goals, working together to complete tasks. Key components include:
- **Agents**: Autonomous AI entities with specific roles and expertise
- **Tasks**: Defined objectives that agents work to complete
- **Tools**: Functions and integrations agents can use
- **Process**: Sequential or hierarchical task execution

## Examples in this Directory

### Content Creation
- **game-builder-crew**: Multi-agent team that designs and builds Python games
- **instagram_post**: Creates engaging Instagram content with research and creativity
- **landing_page_generator**: Builds complete landing pages from concepts
- **marketing_strategy**: Develops comprehensive marketing campaigns
- **screenplay_writer**: Converts text into professional screenplay format

### Business & Productivity
- **job-posting**: Analyzes companies and creates tailored job descriptions
- **prep-for-a-meeting**: Researches participants and prepares meeting strategies
- **recruitment**: Automates candidate sourcing and evaluation
- **stock_analysis**: Performs comprehensive financial analysis with SEC data

### Data & Matching
- **match_profile_to_positions**: CV-to-job matching with vector search
- **meta_quest_knowledge**: Q&A system using PDF documentation

### Travel & Planning
- **surprise_trip**: Plans personalized surprise travel itineraries
- **trip_planner**: Compares destinations and optimizes travel plans

### Template
- **starter_template**: Basic template for creating new CrewAI projects

## Common Crew Patterns

### Agent Definition
```yaml
# agents.yaml
researcher:
  role: "Senior Research Analyst"
  goal: "Uncover cutting-edge developments"
  backstory: "You're a seasoned researcher..."
```

### Task Definition
```yaml
# tasks.yaml
research_task:
  description: "Conduct comprehensive research on {topic}"
  agent: researcher
  expected_output: "Detailed research report"
```

### Crew Assembly
```python
from crewai import Crew, Agent, Task

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process="sequential"  # or "hierarchical"
)
```

## Key Features Demonstrated

1. **Multi-Agent Collaboration**: Examples show 2-7 agents working together
2. **Tool Integration**: Web search, APIs, file manipulation, databases
3. **Custom Tools**: Many examples implement specialized tools
4. **YAML Configuration**: Standardized agent/task definitions
5. **Various Domains**: From creative writing to financial analysis

## Getting Started

1. Choose an example that matches your use case
2. Navigate to its directory
3. Follow the example-specific README
4. Install dependencies (usually via `pip install -r requirements.txt` or `poetry install`)
5. Run with `python main.py` or as specified

Each example is self-contained with all necessary configurations and can be used as a starting point for your own crews.
