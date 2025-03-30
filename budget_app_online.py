import streamlit as st
from streamlit_browser_storage import LocalStorage
from datetime import datetime

# ----------- Config -----------
st.set_page_config(page_title="💳 Smart Budget", layout="centered", page_icon="💳")

# ----------- CSS Styling -----------
st.markdown("""
<style>
body {
    background-color: #f3f6fa;
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #111;
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
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}
.budget-card {
    background-color: white;
    padding: 15px 20px;
    border-radius: 16px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    margin-bottom: 10px;
}
.progress-bar {
    height: 8px;
    border-radius: 8px;
    background-color: #eee;
    overflow: hidden;
}
.progress-bar-fill {
    height: 8px;
    border-radius: 8px;
}
.transaction-card {
    background-color: white;
    padding: 12px 16px;
    border-radius: 14px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
</style>
""", unsafe_allow_html=True)

# ----------- Storage Setup -----------
storage = LocalStorage(key="smart-budget")
balance = storage.get("balance")
transactions = storage.get("transactions")

if not isinstance(balance, (int, float)):
    balance = 400.0
if not isinstance(transactions, list):
    transactions = []

# ----------- Balance Header -----------
st.markdown(f"""
<div class='balance-card'>
    💳 <br>
    Available Balance<br>
    <span style='font-size: 36px; font-weight: bold;'>€{balance:,.2f}</span>
</div>
""", unsafe_allow_html=True)



# ----------- Add Transaction -----------
st.markdown("### ➕ Add Transaction")
amount = st.number_input("Amount", step=0.01, format="%.2f")
desc = st.text_input("Description")
t_type = st.radio("Type", ["Expense", "Income"], horizontal=True)

if st.button("✅ Add", use_container_width=True):
    if amount > 0:
        if t_type == "Expense":
            balance -= amount
            sign = f"-€{amount:.2f}"
        else:
            balance += amount
            sign = f"+€{amount:.2f}"

        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "desc": desc or "(no description)",
            "amount": sign,
            "balance": f"€{balance:.2f}"
        }
        transactions.append(entry)
        storage.set("balance", balance)
        storage.set("transactions", transactions)
        st.experimental_rerun()

# ----------- Transaction History -----------
st.markdown("### 📃 Transactions")

if transactions:
    for tx in reversed(transactions[-10:]):
        st.markdown(f"""
        <div class='transaction-card'>
            <b>{tx['amount']}</b> — {tx['desc']} <br>
            <small>{tx['timestamp']} → <b>{tx['balance']}</b></small>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No transactions yet.")

# ----------- Reset Options -----------
with st.expander("⚙️ Settings"):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Reset All"):
            storage.set("balance", 400.0)
            storage.delete("transactions")
            st.success("App reset.")
            st.experimental_rerun()
    with col2:
        if st.button("Clear Transactions"):
            storage.delete("transactions")
            st.success("Transaction history cleared.")
            st.experimental_rerun()
