import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] : %(message)s")

project_name = "VITO"

files_to_create = [
    ".env",
    ".env.example",
    "requirements.txt",
    "README.md",
    "main.py",
    
    # UI Components
    "streamlit/app.py",
    "streamlit/page_agent.py",
    "streamlit/page_audit.py",
    "streamlit/page_kb.py",
    
    ".gitignore",
    "Dockerfile",

    "src/__init__.py",

    # API Layer
    f"src/{project_name}/api/__init__.py",
    f"src/{project_name}/api/routes.py",
    f"src/{project_name}/api/models.py",

    # LangGraph State Machine
    f"src/{project_name}/graph/__init__.py",
    f"src/{project_name}/graph/state.py",
    f"src/{project_name}/graph/nodes.py",
    f"src/{project_name}/graph/edges.py",
    f"src/{project_name}/graph/workflow.py",

    # Business Logic Services
    f"src/{project_name}/services/__init__.py",
    f"src/{project_name}/services/llm_service.py",
    f"src/{project_name}/services/kb_service.py",
    f"src/{project_name}/services/ticket_service.py",
    f"src/{project_name}/services/audit_service.py",
    f"src/{project_name}/services/validation_service.py",

    # Pydantic Models
    f"src/{project_name}/models/__init__.py",
    f"src/{project_name}/models/ticket.py",
    f"src/{project_name}/models/employee.py",

    # Prompts
    f"src/{project_name}/prompts/__init__.py",
    f"src/{project_name}/prompts/system_prompts.py",

    # Utils
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/logger.py",

    # Mock Data & Persistence
    "data/kb_policies.json",
    "data/employee_requests.csv",
    "data/audit_log.json",

    "tests/__init__.py",
    "tests/test_routing.py",
    "tests/test_kb_retrieval.py",
]

for filepath in files_to_create:
    filepath = Path(filepath)
    folder = filepath.parent

    if folder != Path(""):
        os.makedirs(folder, exist_ok=True)
        logging.info(f"Created folder: {folder}")

    if not filepath.exists():
        filepath.touch()
        logging.info(f"Created file: {filepath}")
    else:
        logging.info(f"File exists: {filepath}")