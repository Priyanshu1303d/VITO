import streamlit as st
import requests

API = "http://localhost:8000"


def render():
    st.header("💬 IT Support Agent")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "emp_name" not in st.session_state:
        st.session_state.emp_name = ""
    st.session_state.emp_name = st.sidebar.text_input(
        "Employee Name", st.session_state.emp_name)
    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if prompt := st.chat_input("Describe your IT issue..."):
        emp = st.session_state.emp_name or "Employee"
        st.session_state.messages.append(
            {"role": "user", "content": f"**{emp}**: {prompt}"})
        with st.chat_message("user"):
            st.markdown(f"**{emp}**: {prompt}")
        with st.spinner("VITO is processing..."):
            try:
                r = requests.post(
                    f"{API}/chat", json={"employee": emp, "message": prompt},
                    timeout=60)
                data = r.json()
            except Exception as e:
                data = {"response_text": f"⚠️ API error: {e}"}
        resp = data.get("response_text", "No response")
        kb = data.get("kb_source", "")
        tid = data.get("ticket_id", "")
        parts = [resp]
        if kb:
            parts.append(f"📚 *KB Source: {kb}*")
        if tid:
            parts.append(f"🎫 *Ticket: {tid}*")
        full = "\n\n".join(parts)
        st.session_state.messages.append({"role": "assistant", "content": full})
        with st.chat_message("assistant"):
            st.markdown(full)
