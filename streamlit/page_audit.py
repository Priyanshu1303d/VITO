import streamlit as st
import requests
import pandas as pd

API = "http://localhost:8000"


def render():
    st.header("📋 Audit Log")
    cols = st.columns([1, 1, 8])
    if cols[0].button("🔄 Refresh"):
        st.rerun()
    if cols[1].button("🗑️ Clear Logs"):
        requests.delete(f"{API}/audit", timeout=10)
        st.rerun()
    try:
        data = requests.get(f"{API}/audit", timeout=10).json()
    except Exception:
        data = []
    if not data:
        st.info("No audit entries yet. Use the Agent to process requests.")
        return
    df = pd.DataFrame(data)
    search = st.text_input("🔍 Search audit log", "")
    if search:
        mask = df.apply(lambda r: search.lower() in str(r).lower(), axis=1)
        df = df[mask]
    st.dataframe(df, use_container_width=True)
