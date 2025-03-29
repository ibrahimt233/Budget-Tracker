import streamlit as st
from streamlit_browser_storage import LocalStorage
from datetime import datetime

# ------------------ App Config ------------------
st.set_page_config(page_title="💶 Balance Tracker", page_icon="💶", layout="centered")
st.markdown("<h1 style='text-align: center;'>📋 Balance Tracker</h1>", unsafe_allow_html=True)

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
st.markdown(
    f"<div style='text-align:center; font-size: 24px;'>💰 Current Balance: <b>€{stored_balance:.2f}</b></div>",
    unsafe_allow_html=True
)

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
with st.container():
    st.markdown("### 🛠️ Manage App")

    if st.button("🔁 Reset Balance & Clear History", use_container_width=True):
        try:
            storage.set("balance", 400.0)
            storage.set("history", [])
            st.session_state.show_reset_msg = True
            st.session_state.show_erased_msg = False
        except Exception as e:
            st.error(f"Reset failed: {e}")
        else:
            st.experimental_rerun()

    if st.button("🗑️ Erase History Only", use_container_width=True):
        try:
            storage.set("history", [])
            st.session_state.show_erased_msg = True
            st.session_state.show_reset_msg = False
        except Exception as e:
            st.error(f"Failed to erase history: {e}")
        else:
            st.experimental_rerun()

# ------------------ Reload Data After Update ------------------
stored_balance = storage.get("balance")
stored_history = storage.get("history")
if not isinstance(stored_history, list):
    stored_history = []

# ------------------ Notification Messages ------------------
if st.session_state.show_reset_msg:
    st.success("Balance reset and history cleared.")
    st.session_state.show_reset_msg = False

elif st.session_state.show_erased_msg:
    st.success("Transaction history erased.")
    st.session_state.show_erased_msg = False

# ------------------ Transaction History ------------------
st.markdown("### 🧾 Transaction History")

if stored_history:
    for item in reversed(stored_history[-10:]):
        st.markdown(
            f"<div style='font-size: 14px;'>🕒 <code>{item['timestamp']}</code><br>"
            f"{item['operation']} | {item['description']} → <b>{item['balance']}</b></div><hr>",
            unsafe_allow_html=True
        )
else:
    st.info("No transactions yet.")
