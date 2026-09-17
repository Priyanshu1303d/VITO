import streamlit as st
import requests
import pandas as pd

API = "http://localhost:8000"


def render():
    st.header("🎫 Ticket Queue")
    if st.button("🔄 Refresh"):
        st.rerun()
    try:
        data = requests.get(f"{API}/tickets", timeout=10).json()
    except Exception:
        data = []
    if not data:
        st.info("No tickets found.")
        return
    df = pd.DataFrame(data)
    tab_open, tab_closed = st.tabs(["🟢 Open", "🔴 Closed"])
    with tab_open:
        odf = df[df["closed"] == False].reset_index(drop=True)
        if odf.empty:
            st.info("No open tickets.")
        else:
            for _, row in odf.iterrows():
                cols = st.columns([1, 2, 3, 3, 1])
                cols[0].markdown(f"**{row['id']}**")
                cols[1].write(row.get("employee", ""))
                cols[2].write(str(row.get("issue", ""))[:60])
                cols[3].write(row.get("status", ""))
                if cols[4].button("✅", key=f"close_{row['id']}",
                                  help="Close this ticket"):
                    requests.patch(f"{API}/tickets/{row['id']}/close",
                                   timeout=10)
                    st.toast(f"Ticket {row['id']} closed!")
                    st.rerun()
    with tab_closed:
        cdf = df[df["closed"] == True]
        if cdf.empty:
            st.info("No closed tickets.")
        else:
            st.dataframe(cdf, use_container_width=True)
