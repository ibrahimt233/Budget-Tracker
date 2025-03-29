import streamlit as st
from streamlit_browser_storage import LocalStorage
from datetime import datetime

# ------------------ App Settings ------------------
st.set_page_config(page_title="💶 Balance Tracker", page_icon="💶", layout="centered")
st.markdown("<h1 style='text-align: center;'>📋 Balance Tracker</h1>", unsafe_allow_html=True)

# ------------------ Storage Setup ------------------
storage = LocalStorage(key="balance-tracker")

# Load balance
try:
    balance = storage.get("balance")
except:
    balance = None
if balance is None:
    balance = 400.0

# Load history
try:
    history = storage.get("history")
except:
    history = []
if not isinstance(history, list):
    history = []

# ------------------ Display Balance ------------------
st.markdown(
    f"<div style='text-align:center; font-size: 24px; margin: 10px 0;'>💰 Current Balance: <b>€{balance:.2f}</b></div>",
    unsafe_allow_html=True
)

# ------------------ Input Form ------------------
with st.container():
    st.markdown("### ➕ Enter a Transaction")
    amount = st.number_input("Amount", step=0.01, format="%.2f")
    description = st.text_input("Description (e.g., groceries)")
    action = st.radio("Action", ["Subtract", "Add"], horizontal=True)

# ------------------ Apply Transaction ------------------
if st.button("✅ Apply Transaction", use_container_width=True) and amount > 0:
    # Remove "History cleared" placeholder if present
    if history and isinstance(history[0], dict) and history[0].get("description") == "History cleared":
        history = []

    if action == "Subtract":
        balance -= amount
        operator = f"-€{amount:.2f}"
    else:
        balance += amount
        operator = f"+€{amount:.2f}"

    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "operation": operator,
        "description": description if description else "(no description)",
        "balance": f"€{balance:.2f}"
    }

    history.append(entry)
    storage.set("balance", balance)
    storage.set("history", history)
    st.experimental_rerun()

# ------------------ Management Buttons ------------------
with st.container():
    st.markdown("### 🛠️ Manage App")

    if st.button("🔁 Reset Balance & Clear History", use_container_width=True):
        storage.set("balance", 400.0)
        storage.set("history", [])
        st.success("Balance reset and history cleared.")
        st.experimental_rerun()

    if st.button("🗑️ Erase History Only", use_container_width=True):
        cleared_entry = [{
            "timestamp": "",
            "operation": "",
            "description": "History cleared",
            "balance": ""
        }]
        storage.set("history", cleared_entry)
        st.success("Transaction history erased!")
        st.experimental_rerun()

# ------------------ Display History ------------------
st.markdown("### 🧾 Transaction History")

if isinstance(history, list) and history and isinstance(history[0], dict):
    if history[0].get("description") == "History cleared":
        st.info("🧹 Transaction history has been erased.")
    else:
        for item in reversed(history[-10:]):
            st.markdown(
                f"<div style='font-size: 14px;'>🕒 <code>{item['timestamp']}</code><br>"
                f"{item['operation']} | {item['description']} → <b>{item['balance']}</b></div><hr>",
                unsafe_allow_html=True
            )
else:
    st.info("No transactions yet.")
