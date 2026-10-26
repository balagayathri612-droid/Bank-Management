import streamlit as st
from hello import Bank

st.set_page_config(page_title="Simple Bank App", layout="centered")
st.title("🏦 Welcome to Streamlit Bank")

menu = st.sidebar.selectbox("Choose Action", ["Create Account", "Deposit", "Withdraw", "Show Details", "Update Info", "Delete Account"])

if menu == "Create Account":
    st.subheader("Create New Account")
    name = st.text_input("Your Name")
    age = st.number_input("Your Age", min_value=0, step=1)
    email = st.text_input("Your Email")
    pin = st.text_input("4-digit PIN", type="password")

    if st.button("Create"):
        if not name.strip() or not email.strip() or not pin.strip():
            st.warning("Fill all fields")
        else:
            try:
                user, msg = Bank.create_account(name.strip(), int(age), email.strip(), int(pin.strip()))
            except ValueError:
                st.error("Age and PIN must be valid numbers")
            else:
                if user:
                    st.success(msg)
                    st.info(f"Your Account Number: {user['accountNo.']}")
                else:
                    st.error(msg)

elif menu == "Deposit":
    st.subheader("Deposit Money")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        if not acc_no.strip() or not pin.strip():
            st.warning("Enter account number and PIN")
        else:
            try:
                success, msg = Bank.deposit(acc_no.strip(), int(pin.strip()), int(amount))
            except ValueError:
                st.error("PIN and amount must be valid numbers")
            else:
                st.success(msg) if success else st.error(msg)

elif menu == "Withdraw":
    st.subheader("Withdraw Money")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        if not acc_no.strip() or not pin.strip():
            st.warning("Enter account number and PIN")
        else:
            try:
                success, msg = Bank.withdraw(acc_no.strip(), int(pin.strip()), int(amount))
            except ValueError:
                st.error("PIN and amount must be valid numbers")
            else:
                st.success(msg) if success else st.error(msg)

elif menu == "Show Details":
    st.subheader("Account Details")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show"):
        if not acc_no.strip() or not pin.strip():
            st.warning("Enter account number and PIN")
        else:
            try:
                user = Bank.find_user(acc_no.strip(), int(pin.strip()))
            except ValueError:
                st.error("PIN must be a valid number")
            else:
                if user:
                    st.json(user)
                else:
                    st.error("No account found")

elif menu == "Update Info":
    st.subheader("Update Your Info")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("Current PIN", type="password")

    name = st.text_input("New Name (Optional)")
    email = st.text_input("New Email (Optional)")
    new_pin = st.text_input("New PIN (Optional)")

    if st.button("Update"):
        if not acc_no.strip() or not pin.strip():
            st.warning("Enter account number and current PIN")
        else:
            cleaned_new_pin = new_pin.strip()
            if cleaned_new_pin and (not cleaned_new_pin.isdigit() or len(cleaned_new_pin) != 4):
                st.warning("New PIN must be exactly 4 digits")
            else:
                try:
                    success, msg = Bank.update_user(acc_no.strip(), int(pin.strip()), name.strip() or None, email.strip() or None, cleaned_new_pin or None)
                except ValueError:
                    st.error("Current PIN must be a valid number")
                else:
                    st.success(msg) if success else st.error(msg)

elif menu == "Delete Account":
    st.subheader("Delete Account")
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        if not acc_no.strip() or not pin.strip():
            st.warning("Enter account number and PIN")
        else:
            try:
                success, msg = Bank.delete_user(acc_no.strip(), int(pin.strip()))
            except ValueError:
                st.error("PIN must be a valid number")
            else:
                st.success(msg) if success else st.error(msg)
