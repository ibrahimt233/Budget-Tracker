import streamlit as st
from streamlit_browser_storage import LocalStorage
from datetime import datetime
from collections import defaultdict

# ------------------ App Config ------------------
st.set_page_config(page_title="💳 Smart Budget", layout="centered", page_icon="💳")

# ------------------ Custom CSS Styling ------------------
st.markdown("""
<style>
body {
    background-color: #f3f6fa;
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #111;
}
.balance-card {
    background: linear-gradient(135deg, #3f51b5, #5c6bc0);
    color: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    font-size: 26px;
    font-weight: 600;
    margin-bottom: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}
.transaction-card {
    background-color: white;
    padding: 15px 20px;
    border-radius: 16px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    margin-bottom: 10px;
    font-size: 15px;
}
.transaction-card small {
    color: gray;
}
.transaction-date {
    margin-top: 25px;
    margin-bottom: 10px;
    font-size: 17px;
    font-weight: bold;
    color: #3f51b5;
}
input, textarea, .stTextInput, .stNumberInput {
    border-radius: 12px !important;
}
.stButton > button {
    border-radius: 12px;
    background-color: #3f51b5;
    color: white;
    font-weight: 500;
    font-size: 16px;
    padding: 0.6em 1.2em;
}
hr {
    border: none;
    border-top: 1px solid #eee;
}
</style>
""", unsafe_allow_html=True)

# ------------------ Setup Browser Storage ------------------
storage = LocalStorage(key="balance-tracker")

# ------------------ Load Data from Browser Storage ------------------
stored_balance = storage.get("balance")
stored_history = storage.get("history")

# Ensure valid types
if not isinstance(stored_balance, (int, float)):
    stored_balance = 400.0

if not isinstance(stored_history, list):
    stored_history = []

# ------------------ Session Flags for Notifications ------------------
if "show_erased_msg" not in st.session_state:
    st.session_state.show_erased_msg = False
if "show_reset_msg" not in st.session_state:
    st.session_state.show_reset_msg = False

# ------------------ Display Current Balance ------------------
st.markdown(f"""
<div class='balance-card'>
    💳 <br>
    Available Balance<br>
    <span style='font-size: 36px; font-weight: bold;'>€{stored_balance:,.2f}</span>
</div>
""", unsafe_allow_html=True)

# ------------------ Transaction Input ------------------
with st.container():
    st.markdown("### ➕ Enter a Transaction")
    amount = st.number_input("Amount", step=0.01, format="%.2f")
    description = st.text_input("Description (e.g., groceries)")
    action = st.radio("Action", ["Subtract", "Add"], horizontal=True)

if st.button("✅ Apply Transaction", use_container_width=True):
    if amount > 0:
        if action == "Subtract":
            new_balance = stored_balance - amount
            operator = f"-€{amount:.2f}"
        else:
            new_balance = stored_balance + amount
            operator = f"+€{amount:.2f}"

        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operation": operator,
            "description": description if description else "(no description)",
            "balance": f"€{new_balance:.2f}"
        }

        new_history = stored_history + [entry]

        try:
            storage.set("balance", new_balance)
            storage.set("history", new_history)
        except Exception as e:
            st.error(f"Failed to save data: {e}")
        else:
            st.success("Transaction added.")
            st.experimental_rerun()

# ------------------ Manage Buttons ------------------
with st
