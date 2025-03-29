import streamlit as st
from streamlit_browser_storage import LocalStorage
from datetime import datetime

st.set_page_config(page_title="💶 Balance Tracker", page_icon="💶")
st.title("💶 Balance Tracker")

# Initialize LocalStorage
storage = LocalStorage(key="balance-tracker-data")

# Get current balance or set default
try:
    balance = storage.get("balance")
except Exception:
    balance = None

if balance is None:
    balance = 400.0

# Get transaction history
try:
    history = storage.get("history")
except Exception:
    history = []

if history is None:
    history = []

st.markdown(f"### 💰 Current Balance: **€{balance:.2f}**")

# User input
transaction = st.number_input("Enter amount", step=0.01, format="%.2f")
action = st.radio("Choose action", ["Subtract", "Add"])

col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Apply Transaction"):
        if action == "Subtract":
            balance -= transaction
            operation = f"-€{transaction:.2f}"
        else:
            balance += transaction
            operation = f"+€{transaction:.2f}"

        # Save new balance
        storage.set("balance", balance)

        # Add to history
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history.append(f"{timestamp} | {operation} → New balance: €{balance:.2f}")
        storage.set("history", history)

        st.experimental_rerun()

with col2:
    if st.button("🔁 Reset Balance"):
        balance = 400.0
        storage.set("balance", balance)
        storage.set("history", [])
        st.experimental_rerun()

# Show transaction history
st.markdown("### 🧾 Transaction History")
if history:
    for item in reversed(history[-10:]):  # Show last 10 transactions
        st.markdown(f"- {item}")
else:
    st.write("No transactions yet.")
