
# HealthConnect: AI-Powered Healthcare Assistant with Fetch.ai uAgents

HealthConnect is a modular, AI-powered healthcare assistant built using the Fetch.ai uAgents framework. It allows users to interact with specialized agents for symptoms, medications, and appointments — all through a command-line interface (CLI). These agents communicate asynchronously via Agentverse.

## Features

- Natural language interface for healthcare queries
- Modular agent-based design
- Asynchronous messaging using the uAgents mailbox system
- AI-powered backend responses using the ASI-1 Mini inference agent
- Clean CLI interface with real-time feedback

## Architecture Overview

```
User (CLI)
   │
   └──> app.py (CLI Agent)
         │
         ├──> symptom_agent.py ───> ASI Agent ─┐
         ├──> medication_agent.py ──> ASI Agent ┤
         └──> appointment_agent.py ─> ASI Agent ┘
                     │
                  <──┘ (response sent back to CLI)
```

## How It Works

1. User submits a health-related query through the CLI.
2. The CLI (app.py) routes the query to the appropriate agent based on keywords.
3. The agent constructs a prompt and sends it to the ASI-1 Mini inference agent.
4. ASI agent generates a smart response.
5. The agent returns the response back to the CLI.
6. The CLI displays the result to the user.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/healthconnect.git
cd healthconnect
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Agents

Each agent must be started in its own terminal:

```bash
python symptom_agent.py
python medication_agent.py
python appointment_agent.py
```

### 4. Run the CLI

```bash
python app.py
```

Then enter queries like:

```
I have a sore throat and fever.
Remind me to take my medicine at 8 PM.
Book a follow-up appointment for next week.
```

## Project Structure

```
healthconnect/
├── app.py                   # CLI agent for sending queries and printing responses
├── appointment_agent.py     # Processes appointment-related queries and talks to ASI agent
├── medication_agent.py      # Handles medication reminders and queries
├── symptom_agent.py         # Processes symptom analysis requests
```

## Status

- [x] CLI agent connected to Agentverse agents
- [x] Functional symptom, medication, and appointment agents
- [x] AI-generated replies using ASI-1 Mini
- [ ] Optional: Web-based UI with Streamlit (future)
- [ ] Optional: Integration with calendars or health APIs

## Acknowledgments

- [Fetch.ai](https://fetch.ai) for the uAgents framework and Agentverse infrastructure
- ASI-1 Mini agent for backend AI responses
