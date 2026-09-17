import streamlit as st
import json
from pathlib import Path

_KB_PATH = Path(__file__).resolve().parents[1] / "data" / "kb_policies.json"


def render():
    st.header("📚 Knowledge Base Policies")
    policies = json.loads(_KB_PATH.read_text())
    for p in policies:
        with st.expander(f"**{p['id']}** — {p['title']}  ({p['category']})"):
            st.write(p["content"])
            cols = st.columns(3)
            cols[0].caption(f"Authority: {p['authority']}")
            cols[1].caption(f"Ticket required: {p['requires_ticket']}")
            cols[2].caption(f"Category: {p['category']}")
