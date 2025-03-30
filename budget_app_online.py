import streamlit as st
from streamlit_browser_storage import LocalStorage
from datetime import datetime

# ------------------ Page Setup ------------------
st.set_page_config(page_title="💶 Budget Tracker", page_icon="💶", layout="centered")

# ------------------ Custom Styles ------------------
st.markdown("""
<style>
body {
    background-color: #f7f9fc;
    color: #111;
}
h1 {
    text-align: center;
}
.balance-box {
    background: linear-gradient(145deg, #e3edf7, #ffffff);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    margin-top: 20px;
}
.transaction-card {
    background-color: white;
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.transaction-card small {
    color: gray;
}
.stButton > button {
    border-radius: 12px;
    padding: 0.75em;
    font-size: 16px;
    font-weight: 500;
}
hr {
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ------------------ Storage ------------------
storage = LocalStorage(key="balance-tracker")

# ------------------ Load Stored Data ------------------
stored_balance = storage.get("balance")
stored_history = storage.get("history")

if not isinstance(stored_balance, (int, float)):
    stored_balance = 400.0
if not isinstance(stored_history, list):
    stored_history = []

# ------------------ Session Flags ------------------
if "show_erased_msg" not in st.session_state:
    st.session_state.show_erased_msg = False
if "show_reset_msg" not in st.session_state:
    st.session_state.show_reset_msg = False

# ------------------ App Title ------------------
st.markdown("<h1>📋 Budget Tracker</h1>", unsafe_allow_html=True)

# ------------------ Balance Display ------------------
st.markdown(f"<div class='balance-box'>💰 Balance: €{stored_balance:.2f}</div>", unsafe_allow_html=True)

# ------------------ Add Transaction ------------------
with st.container():
    st.markdown("### ➕ New Transaction")
    amount = st.number_input("Amount", step=0.01, format="%.2f")
    description = st.text_input("Description (e.g., groceries)")
    action = st.radio("Type", ["Subtract", "Add"], horizontal=True)

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

# ------------------ Management Buttons ------------------
with st.container():
    st.markdown("### 🛠️ Manage")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Reset Balance & History", use_container_width=True):
            try:
                storage.set("balance", 400.0)
                storage.delete("history")
                st.session_state.show_reset_msg = True
                st.session_state.show_erased_msg = False
            except Exception as e:
                st.error(f"Reset failed: {e}")
            else:
                st.experimental_rerun()

    with col2:
        if st.button("🗑️ Erase History Only", use_container_width=True):
            try:
                storage.delete("history")
                st.session_state.show_erased_msg = True
                st.session_state.show_reset_msg = False
            except Exception as e:
                st.error(f"Failed to erase history: {e}")
            else:
                st.experimental_rerun()

# ------------------ Refresh Stored Data ------------------
stored_balance = storage.get("balance")
stored_history = storage.get("history")
if not isinstance(stored_history, list):
    stored_history = []

# ------------------ Messages ------------------
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
        st.markdown(f"""
        <div class='transaction-card'>
            <b>{item['operation']}</b> — {item['description']}<br>
            <small>{item['timestamp']} → <b>{item['balance']}</b></small>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No transactions yet.")
