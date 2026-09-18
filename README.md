# VITO - Veridian IT Orchestrator

VITO (Veridian IT Orchestrator) is an AI-powered internal IT support agent for **Veridian Corp**.

It uses **LangGraph** to orchestrate an IT support workflow, **Groq** for LLM-based classification and decision-making, **FastAPI** for the backend API, and **Streamlit** for the web interface.

VITO can classify employee IT issues, retrieve relevant knowledge-base policies, decide whether an issue should be resolved, converted into a ticket, escalated, or require additional information, and maintain an audit trail of processed requests.

---

## How VITO Works

When an employee submits an IT issue, VITO processes it through a LangGraph workflow:

```mermaid
graph TD
    A[START] --> B[classify_issue]
    B --> C[retrieve_policy]
    C --> D[decide_action]

    D -->|followup| E[ask_followup]
    E --> F[END]

    D -->|ticket / self_service| G[resolve_request]
    D -->|escalate| H[escalate_request]

    G --> I[validate_output]
    H --> I

    I --> J[create_ticket]
    J --> K[write_audit]
    K --> F
````

---

## Supported IT Categories

VITO's classifier supports the following categories:

* `vpn`
* `password`
* `laptop`
* `software`
* `printer`
* `mailbox`
* `guest_wifi`
* `expense_tool`
* `security_incident`
* `wfh_equipment`
* `admin_access`
* `unclear`

---

## Decision Rules

VITO uses predefined rules in its system prompt to guide the action decision.

| Situation                                  | Action         |
| ------------------------------------------ | -------------- |
| Security incident such as phishing/malware | `escalate`     |
| Admin access request                       | `escalate`     |
| Unclear request or missing information     | `followup`     |
| Password reset                             | `self_service` |
| Guest Wi-Fi issue                          | `self_service` |
| Laptop age >= 3 years                      | `ticket`       |
| Laptop age < 3 years                       | `escalate`     |
| Other resolvable IT issues                 | `ticket`       |

The response is also instructed to cite the relevant KB policy IDs used during decision-making.

---

## Tech Stack

| Component           | Technology            |
| ------------------- | --------------------- |
| Language            | Python                |
| LLM                 | Groq                  |
| Model               | `openai/gpt-oss-120b` |
| Agent Orchestration | LangGraph             |
| LLM Framework       | LangChain             |
| Backend             | FastAPI               |
| ASGI Server         | Uvicorn               |
| Frontend            | Streamlit             |
| Data Validation     | Pydantic v2           |
| Data Processing     | Pandas                |
| Persistence         | JSON files            |
| Testing             | Pytest                |
| Configuration       | python-dotenv         |

---

## Project Structure

```text
VITO/
│
├── README.md
├── Dockerfile
├── LICENSE
├── main.py
├── requirements.txt
├── setup.py
├── template.py
├── .env.example
├── run.bat (use this to run the project with one command in terminal run.bat)
│
├── src/
│   ├── __init__.py
│   │
│   └── VITO/
│       ├── __init__.py
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── routes.py
│       │
│       ├── graph/
│       │   ├── __init__.py
│       │   ├── edges.py
│       │   ├── nodes.py
│       │   ├── state.py
│       │   └── workflow.py
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── employee.py
│       │   └── ticket.py
│       │
│       ├── prompts/
│       │   ├── __init__.py
│       │   └── system_prompts.py
│       │
│       ├── services/
│       │   ├── __init__.py
│       │   ├── audit_service.py
│       │   ├── kb_service.py
│       │   ├── llm_service.py
│       │   ├── ticket_service.py
│       │   └── validation_service.py
│       │
│       └── utils/
│           ├── __init__.py
│           └── logger.py
│
├── streamlit/
│   ├── app.py
│   ├── page_agent.py
│   ├── page_audit.py
│   ├── page_kb.py
│   ├── page_tickets.py
│   └── .streamlit/
│       └── config.toml
│
└── tests/
    ├── __init__.py
    ├── test_kb_retrieval.py
    └── test_routing.py
```

> **Note:** The application expects a `data/` directory containing the knowledge-base and JSON persistence files used by the services.

---

## API Endpoints

| Method   | Endpoint                     | Description                    |
| -------- | ---------------------------- | ------------------------------ |
| `GET`    | `/`                          | Health/status endpoint         |
| `POST`   | `/chat`                      | Process an employee IT request |
| `GET`    | `/tickets`                   | Retrieve all tickets           |
| `PATCH`  | `/tickets/{ticket_id}/close` | Close an open ticket           |
| `GET`    | `/audit`                     | Retrieve the audit log         |
| `DELETE` | `/audit`                     | Clear the audit log            |

---

## API Example

### Send an IT Request

**Request**

```http
POST /chat
Content-Type: application/json
```

```json
{
  "employee": "John Doe",
  "message": "I forgot my password and cannot log in."
}
```

### Response

```json
{
  "response_text": "Per KB-01, ...",
  "action": "self_service",
  "category": "password",
  "kb_source": "KB-01",
  "ticket_id": "",
  "escalation_reason": ""
}
```

The exact response content depends on the LLM output and the retrieved knowledge-base policies.

---

## Prerequisites

Make sure you have:

* Python 3.10+
* A Groq API key
* `pip`

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Priyanshu1303d/VITO.git
cd VITO
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate

# or you can use uv
uv venv .venv --python 3.11
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The requirements file also installs the local VITO package in editable mode.

---

## Environment Variables

Create a `.env` file from the provided example:

```bash
cp .env.example .env
```

On Windows, you can also create the file manually.

Add your Groq API key:

```env
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL_NAME=openai/gpt-oss-120b
```

### Environment Variables

| Variable          | Description                         |
| ----------------- | ----------------------------------- |
| `GROQ_API_KEY`    | API key used to access the Groq LLM |
| `GROQ_MODEL_NAME` | Groq model used by VITO             |

---

## Running the Application

### Local Setup
Windows One-Click Launcher

For Windows users, VITO includes a one-click launcher that automatically sets up the Python environment, installs dependencies, and starts both the FastAPI backend and Streamlit frontend. 

Run this command:

```bash
run.bat
```

The launcher will:

1. Create a Python 3.11 virtual environment using `uv` if `.venv` does not exist.
2. Install the required dependencies from `requirements.txt`.
3. Start the FastAPI backend on `http://localhost:8000`.
4. Start the Streamlit frontend on `http://localhost:8501`.

### Manual Setup

If you prefer to run the services manually:

```bash
# Create virtual environment
uv venv .venv --python 3.11

# Install dependencies
uv pip install --python .venv\Scripts\python.exe -r requirements.txt

# Start FastAPI
.venv\Scripts\uvicorn.exe main:app --reload --port 8000

# Start Streamlit (in a new terminal)
.venv\Scripts\activate
streamlit run streamlit/app.py
```

> **Prerequisite:** Make sure [uv](https://docs.astral.sh/uv/) is installed and available in your PATH.
---

## Data Storage

VITO currently uses local JSON files for persistence rather than a database.

The services expect data under:

```text
data/
```

The application uses files such as:

```text
data/kb_policies.json
data/ticket_queue.json
data/audit_log.json
```

### Knowledge Base

`kb_policies.json` contains the IT policies used by VITO when processing employee requests.

The KB service filters policies by the classified issue category.

### Tickets

Tickets are stored in:

```text
data/ticket_queue.json
```

Each ticket contains information such as:

```json
{
  "id": "TK-1051",
  "employee": "John Doe",
  "issue": "Laptop is not working",
  "status": "ticket",
  "category": "laptop",
  "kb_source": "KB-03",
  "resolution": "...",
  "closed": false
}
```
---

## Design Principles

VITO separates the application into several layers:

```text
Streamlit UI
     ↓
FastAPI API
     ↓
LangGraph Workflow
     ↓
Services
     ├── LLM Service
     ├── KB Service
     ├── Ticket Service
     ├── Validation Service
     └── Audit Service
     ↓
JSON Persistence
```

This separation keeps the workflow logic, API layer, business services, and UI components independent from each other.

---

## Current Limitations

This project is currently designed as a prototype/internal demonstration rather than a production-ready enterprise IT service.

Some current limitations include:

* JSON files are used instead of a database.
* Prompt-injection detection uses keyword matching.
* PII masking uses regular expressions
* Authentication and authorization are not implemented.
* The application assumes the required data files are available locally.

These limitations should be addressed before deploying VITO as a production enterprise IT support system.

---

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---
# Author

<div align="center">
  <i>Architected & Built by Priyanshu · 2026</i>
</div>
