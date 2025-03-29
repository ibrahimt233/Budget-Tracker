import streamlit as st
from streamlit_browser_storage import LocalStorage
from datetime import datetime

st.set_page_config(page_title="💶 Balance Tracker", page_icon="💶")
st.title("💶 Balance Tracker")

# Initialize browser storage
storage = LocalStorage(key="balance-tracker")

# Get current balance
try:
    balance = storage.get("balance")
except Exception:
    balance = None

if balance is None:
    balance = 400.0

# Get transaction history (as a list of dictionaries)
try:
    history = storage.get("history")
except Exception:
    history = []

if not isinstance(history, list):
    history = []

# Show current balance
st.markdown(f"### 💰 Current Balance: **€{balance:.2f}**")

# --- Input fields ---
transaction = st.number_input("Enter amount", step=0.01, format="%.2f")
description = st.text_input("Enter description (e.g., groceries, rent)")
action = st.radio("Choose action", ["Subtract", "Add"])

col1, col2 = st.columns(2)

# --- Apply Transaction ---
with col1:
    if st.button("✅ Apply Transaction") and transaction > 0:
        if action == "Subtract":
            balance -= transaction
            operation = f"-€{transaction:.2f}"
        else:
            balance += transaction
            operation = f"+€{transaction:.2f}"

        # Save new balance
        storage.set("balance", balance)

        # Build history entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "operation": operation,
            "description": description,
            "balance": f"€{balance:.2f}"
        }

        # Update history
        history.append(entry)
        storage.set
