import streamlit as st
from streamlit_browser_storage import LocalStorage

st.set_page_config(page_title="Balance Tracker", page_icon="💶")
st.title("💶 Balance Tracker")

# 🟩 Get balance from browser storage
storage = LocalStorage(key="balance-storage")
value = storage.values.get("balance")
if value is None:
    balance = 400.0
else:
    balance = value

st.write(f"### Current Balance: €{balance:.2f}")

# Input
transaction = st.number_input("Enter transaction amount", step=0.01, format="%.2f")

# 🟦 Apply transaction
if st.button("Apply Transaction"):
    balance -= transaction
    storage.set("balance", balance)
    st.experimental_rerun()

# 🟦 Reset balance
if st.button("Reset Balance"):
    balance = 400.0
    storage.set("balance", balance)
    st.experimental_rerun()
