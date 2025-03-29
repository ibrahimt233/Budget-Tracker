import streamlit as st
from streamlit_browser_storage import LocalStorage
from datetime import datetime

# ------------------ App Settings ------------------
st.set_page_config(page_title="💶 Balance Tracker", page_icon="💶", layout="centered")
st.markdown("<h1 style='text-align: center;'>📋 Balance Tracker</h1>", unsafe_allow_html=True)

# ------------------ Browser Storage ------------------
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
st.markdown(f"<h3 style='text-align: center;'>💰 Current Balance: €{balance:.2f}</h3>", unsafe_allow_html=True)

# ------------------ User Input ------------------
st.markdown("### ➕ Enter a Transaction")
amount = st.number_input("Enter amount", step=0.01, format="%.2f")
description = st.text_input("Enter description (e.g., groceries, rent)")
action = st.radio("Choose action", ["Subtract", "Add"])

col1, col2 = st.columns(2)

# ------------------ Apply Transaction ------------------
with col1:
    if st.button("✅ Apply Transaction") and amount > 0:
        if action == "Subtract":
            balance -= amount
            operator = f"-€{amount:.2f}"
        else:
            balance += amount
            operator = f"+€{amount:.2f}"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "operation": operator,
            "description": description if description else "(no description)",
            "balance": f"€{balance:.2f}"
        }

        history.append(entry)
        storage.set("balance", balance)
        storage.set("history", history)
        st.experimental_rerun()

# ------------------ Reset Balance ------------------
with col2:
    if st.button("🔁 Reset Balance"):
        storage.set("balance", 400.0)
        storage.set("history", [])
        st.success("Balance reset and history cleared.")
        st.experimental_rerun()

# ------------------ Erase History Only ------------------
col3, _ = st.columns(2)
with col3:
    if st.button("🗑️ Erase History Only"):
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
st.markdown("### 🧾 Transaction History (Last 10)")

if isinstance(history, list) and history and isinstance(history[0], dict):
    if history[0]["description"] == "History cleared":
        st.info("🧹 Transaction history has been erased.")
    else:
        for item in reversed(history[-10:]):
            st.markdown(
                f"- `{item['timestamp']}` | **{item['operation']}** | {item['description']} → {item['balance']}"
            )
else:
    st.info("No transactions yet.")
