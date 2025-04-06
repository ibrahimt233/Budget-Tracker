import streamlit as st
from streamlit_browser_storage import LocalStorage
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt

# ------------------ App Config ------------------
st.set_page_config(page_title="💳 Smart Budget", layout="centered", page_icon="💳")

# ------------------ Custom CSS ------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom, #000000, #2c2c2c);
    font-family: 'Segoe UI', sans-serif;
    color: #f1f1f1;
}
h1, h2, h3 {
    color: #ffffff;
}
.balance-card {
    background: linear-gradient(135deg, #3f51b5, #5c6bc0);
    color: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    font-size: 26px;
    font-weight: 600;
    margin-bottom: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}
.transaction-card {
    background-color: #1e1e1e;
    padding: 15px 20px;
    border-radius: 16px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    margin-bottom: 10px;
    font-size: 15px;
}
.transaction-card .desc {
    color: #ff4c4c;
    font-weight: 500;
}
.transaction-card .amount.income {
    color: #00e676;
    font-weight: bold;
}
.transaction-card .amount.expense {
    color: #ff4c4c;
    font-weight: bold;
}
.transaction-card small {
    color: #bbbbbb;
}
.transaction-date {
    margin-top: 25px;
    margin-bottom: 10px;
    font-size: 17px;
    font-weight: bold;
    color: #80d8ff;
}
</style>
""", unsafe_allow_html=True)

# ------------------ Setup Browser Storage ------------------
storage = LocalStorage(key="balance-tracker")

# ------------------ Load Data ------------------
stored_balance = storage.get("balance")
stored_history = storage.get("history")
weekly_allowance = storage.get("weekly_allowance")

if not isinstance(stored_balance, (int, float)):
    stored_balance = 400.0
if not isinstance(stored_history, list):
    stored_history = []
if not isinstance(weekly_allowance, (int, float)):
    weekly_allowance = 100.0

# ------------------ Session Flags ------------------
if "show_erased_msg" not in st.session_state:
    st.session_state.show_erased_msg = False
if "show_reset_msg" not in st.session_state:
    st.session_state.show_reset_msg = False

# ------------------ Weekly Allowance Setup ------------------
with st.sidebar:
    st.markdown("### 🗓️ Weekly Allowance")
    weekly_allowance_input = st.number_input("Set your weekly allowance (€)", value=weekly_allowance, step=1.0)
    if weekly_allowance_input != weekly_allowance:
        weekly_allowance = weekly_allowance_input
        storage.set("weekly_allowance", weekly_allowance)

# ------------------ Display Balance ------------------
st.markdown(f"""
<div class='balance-card'>
    💳 <br>
    Available Balance<br>
    <span style='font-size: 36px; font-weight: bold;'>€{stored_balance:,.2f}</span>
</div>
""", unsafe_allow_html=True)

# ------------------ Weekly Spending Pie Chart ------------------
st.markdown("### 📊 Weekly Spending Overview")

# Filter expenses from current week
today = datetime.today()
start_of_week = today - timedelta(days=today.weekday())  # Monday

weekly_spending = 0.0
for tx in stored_history:
    tx_time = datetime.strptime(tx["timestamp"], "%Y-%m-%d %H:%M:%S")
    if tx_time >= start_of_week and tx["operation"].startswith("-"):
        amount = float(tx["operation"].replace("€", "").replace("-", ""))
        weekly_spending += amount

remaining = max(0, weekly_allowance - weekly_spending)
spent = min(weekly_spending, weekly_allowance)

# Pie chart
fig, ax = plt.subplots()
ax.pie([spent, remaining],
       labels=["Spent", "Left"],
       colors=["#ff4c4c", "#00e676"],
       startangle=90,
       autopct='%1.1f%%',
       wedgeprops={'edgecolor': 'black'})
ax.axis("equal")
st.pyplot(fig)

st.markdown(f"**Spent this week:** €{spent:.2f} / €{weekly_allowance:.2f}")

# ------------------ Input Section ------------------
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
st.markdown("### 🛠️ Manage App")

if st.button("🔁 Reset Balance & Clear History", use_container_width=True):
    try:
        storage.set("balance", 400.0)
        storage.delete("history")
        st.session_state.show_reset_msg = True
        st.session_state.show_erased_msg = False
    except Exception as e:
        st.error(f"Reset failed: {e}")
    else:
        st.experimental_rerun()

if st.button("🗑️ Erase History Only", use_container_width=True):
    try:
        storage.delete("history")
        st.session_state.show_erased_msg = True
        st.session_state.show_reset_msg = False
    except Exception as e:
        st.error(f"Failed to erase history: {e}")
    else:
        st.experimental_rerun()

# ------------------ Reload Data After Action ------------------
stored_balance = storage.get("balance")
stored_history = storage.get("history")
if not isinstance(stored_history, list):
    stored_history = []

# ------------------ Notifications ------------------
if st.session_state.show_reset_msg:
    st.success("Balance reset and history cleared.")
    st.session_state.show_reset_msg = False
elif st.session_state.show_erased_msg:
    st.success("Transaction history erased.")
    st.session_state.show_erased_msg = False

# ------------------ Calendar View ------------------
st.markdown("### 🗓️ Transaction Calendar")

if stored_history:
    grouped = defaultdict(list)
    for item in stored_history:
        date = item['timestamp'].split(' ')[0]
        grouped[date].append(item)

    for date in sorted(grouped.keys(), reverse=True):
        st.markdown(f"<div class='transaction-date'>{date}</div>", unsafe_allow_html=True)
        for tx in grouped[date]:
            is_income = tx["operation"].startswith("+")
            amount_class = "income" if is_income else "expense"
            st.markdown(f"""
            <div class='transaction-card'>
                <span class='amount {amount_class}'>{tx['operation']}</span>
                — <span class='desc'>{tx['description']}</span><br>
                <small>{tx['timestamp']} → <b>{tx['balance']}</b></small>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("No transactions yet.")
