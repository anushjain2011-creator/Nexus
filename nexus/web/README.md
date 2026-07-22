# Nexus Dashboard

React + CSS dashboard that polls the Nexus API server and shows the
`WorldModel` live: tasks, budget, risks, knowledge, and a scrolling ticker
of `EventBus` activity.

## Run

**1. Start the API server** (from the repo root):
    pip install -r requirements.txt
    cp .env.example .env   # fill in OPENAI_API_KEY / OPENAI_BASE_URL / OPENAI_MODEL
    python -m server.app

This serves the API at http://localhost:8000.

**2. Start the dashboard** (from web/):
    npm install
    npm run dev

Opens at http://localhost:5173.

## Using it

- Type a goal in the top bar and hit Run — the Executive agent
  bootstraps tasks, a budget breakdown, and initial risks.
- Type a problem (e.g. "Our hardware supplier just failed") under
  "Inject a problem" and hit Trigger — watch Research/Planning/Risk
  agents adapt the plan.
- The ticker at the bottom shows every event published on the EventBus
  as it happens.
- "Reset project" clears state for a fresh demo run.

## Config

Point the dashboard at a different API host with VITE_API_BASE in web/.env:
    VITE_API_BASE=http://localhost:8000
