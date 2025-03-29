import streamlit as st
from streamlit_browser_storage import LocalStorage
from datetime import datetime

st.set_page_config(page_title="💶 Balance Tracker", page_icon="💶", layout="centered")
st.markdown("<h1 style='text-align: center;'>📋 Balance Tracker</h1>", unsafe_allow_html=True)

# Initialize LocalStorage with a key
storage = LocalStorage(key="balance-tracker")

# Get stored balance or default to 400
try:
    balance = storage.get("balance")
except:
    balance = None
if balance is None:
    balance = 400.0

# Get stored history or empty list
try:
    history = storage.get("history")
except:
    history = []

# Make sure history is a list
if not isinstance(history, list):
    history = []

# 💰 Display current balance
st.markdown(f"<h3 style='text-align: center;'>💰 Current Balance: €{balance:.2f}</h3>", unsafe_allow_html=True)

# 📥 Transaction input
st.markdown("### ➕ Enter a transaction")
amount = st.number_input("Enter amount", step=0.01, format="%.2f")
description = st.text_input("Enter description (e.g., groceries, rent)")
action = st.radio("Choose action", ["Subtract", "Add"])

col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Apply Transaction") and amount > 0:
        # logic as before...

with col2:
    if st.button("🔁 Reset Balance"):
        storage.set("balance", 400.0)
        storage.set("history", [])
        st.experimental_rerun()

col3, _ = st.columns(2)
with col3:
    if st.button("🗑️ Erase History Only"):
        history = []  # fix: reset local variable too
        storage.set("history", history)
        st.success("Transaction history erased!")
        st.experimental_rerun()


# 🔁 Reset
with col2:
    if st.button("🔁 Reset Balance"):
        storage.set("balance", 400.0)
        storage.set("history", [])
        st.experimental_rerun()

col3, _ = st.columns(2)

with col3:
    if st.button("🗑️ Erase History Only"):
        storage.set("history", [])
        st.success("Transaction history erased!")
        st.experimental_rerun()


# 🧾 Show history
st.markdown("### 🧾 Transaction History (Last 10)")
if history:
    for item in reversed(history[-10:]):
        st.markdown(
            f"- `{item['timestamp']}` | **{item['operation']}** | {item['description']} → {item['balance']}"
        )
else:
    st.info("No transactions yet.")
