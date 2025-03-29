import streamlit as st
from streamlit_browser_storage import LocalStorage

st.set_page_config(page_title="Balance Tracker", page_icon="💶")
st.title("💶 Balance Tracker")

# Create local storage with a key (required)
storage = LocalStorage(key="balance-storage")

# Get saved balance from browser, or set to default
balance = storage.get_value("balance")
if balance is None:
    balance = 400.0

st.write(f"### Current Balance: €{balance:.2f}")

# Input for transaction
transaction = st.number_input("Enter transaction amount", step=0.01, format="%.2f")

# Apply transaction
if st.button("Apply Transaction"):
    balance -= transaction
    storage.set_value("balance", balance)
    st.experimental_rerun()

# Reset balance
if st.button("Reset Balance"):
    balance = 400.0
    storage.set_value("balance", balance)
    st.experimental_rerun()
