import streamlit as st

st.set_page_config(
    page_title="VITO — IT Support", page_icon="🤖",
    layout="wide", initial_sidebar_state="expanded",
)

st.sidebar.title("🤖 VITO")
st.sidebar.caption("Veridian IT Orchestrator")
page = st.sidebar.radio(
    "Navigate", ["💬 Agent", "🎫 Tickets", "📋 Audit Log", "📚 KB Policies"]
)

if page == "💬 Agent":
    from page_agent import render
    render()
elif page == "🎫 Tickets":
    from page_tickets import render
    render()
elif page == "📋 Audit Log":
    from page_audit import render
    render()
else:
    from page_kb import render
    render()
