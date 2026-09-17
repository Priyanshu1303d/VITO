import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from VITO.utils.logger import get_logger

load_dotenv()
log = get_logger(__name__)
_model = os.getenv("GROQ_MODEL_NAME", "openai/gpt-oss-120b")
_llm = ChatGroq(model=_model)


def call_llm(prompt: str) -> str:
    log.info("LLM call: %s...", prompt[:60])
    return _llm.invoke(prompt).content


def call_llm_structured(prompt: str, schema):
    log.info("Structured LLM call → %s", schema.__name__)
    return _llm.with_structured_output(schema).invoke(prompt)
