import streamlit as st

st.set_page_config(page_title="Balance Tracker", page_icon="💶")
st.title("💶 Balance Tracker")

# Initialize balance
if "balance" not in st.session_state:
    st.session_state.balance = 400.0

st.write(f"### Current Balance: €{st.session_state.balance:.2f}")

# Input for transaction
transaction = st.number_input("Enter transaction amount", step=0.01, format="%.2f")

# Apply transaction
if st.button("Apply Transaction"):
    st.session_state.balance -= transaction
    st.experimental_rerun()

# Reset balance
if st.button("Reset Balance"):
    st.session_state.balance = 400.0
    st.experimental_rerun()