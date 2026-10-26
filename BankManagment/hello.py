import json
import random
import string
from pathlib import Path

#created using chatGPT
class Bank:
    database = 'data.json'
    
    @classmethod
    def load_data(cls):
        if Path(cls.database).exists():
            with open(cls.database, 'r') as fs:
                return json.load(fs)
        return []

    @classmethod
    def save_data(cls, data):
        with open(cls.database, 'w') as fs:
            json.dump(data, fs, indent=4)

    @classmethod
    def generate_account_number(cls):
        chars = random.choices(string.ascii_letters, k=3) + \
                random.choices(string.digits, k=3) + \
                random.choices("!@#$%^&*", k=1)
        random.shuffle(chars)
        return ''.join(chars)

    @staticmethod
    def _coerce_int(value, field_name):
        if value is None:
            raise ValueError(f"{field_name} is required")
        try:
            return int(value)
        except (TypeError, ValueError):
            raise ValueError(f"{field_name} must be a valid integer")

    @classmethod
    def create_account(cls, name, age, email, pin):
        data = cls.load_data()
        if not name or not email:
            return None, "Name and email are required"
        try:
            age_value = cls._coerce_int(age, "Age")
            pin_value = cls._coerce_int(pin, "PIN")
        except ValueError as exc:
            return None, str(exc)

        if age_value < 18 or len(str(abs(pin_value))) != 4:
            return None, "Age must be 18+ and PIN should be 4 digits"

        acc_no = cls.generate_account_number()
        user = {
            "name": name,
            "age": age_value,
            "email": email,
            "pin": pin_value,
            "accountNo.": acc_no,
            "balance": 0
        }
        data.append(user)
        cls.save_data(data)
        return user, f"Account created successfully. Your Account Number: {acc_no}"

    @classmethod
    def find_user(cls, acc_no, pin):
        data = cls.load_data()
        try:
            pin_value = cls._coerce_int(pin, "PIN")
        except ValueError:
            return None

        for user in data:
            if user['accountNo.'] == acc_no and user['pin'] == pin_value:
                return user
        return None

    @classmethod
    def deposit(cls, acc_no, pin, amount):
        data = cls.load_data()
        try:
            pin_value = cls._coerce_int(pin, "PIN")
            amount_value = cls._coerce_int(amount, "Amount")
        except ValueError as exc:
            return False, str(exc)

        for user in data:
            if user['accountNo.'] == acc_no and user['pin'] == pin_value:
                if 0 < amount_value <= 10000:
                    user['balance'] += amount_value
                    cls.save_data(data)
                    return True, "Deposit successful"
                return False, "Amount must be between 1 and 10000"
        return False, "Invalid account or PIN"

    @classmethod
    def withdraw(cls, acc_no, pin, amount):
        data = cls.load_data()
        try:
            pin_value = cls._coerce_int(pin, "PIN")
            amount_value = cls._coerce_int(amount, "Amount")
        except ValueError as exc:
            return False, str(exc)

        for user in data:
            if user['accountNo.'] == acc_no and user['pin'] == pin_value:
                if amount_value <= 0:
                    return False, "Amount must be greater than zero"
                if user['balance'] >= amount_value:
                    user['balance'] -= amount_value
                    cls.save_data(data)
                    return True, "Withdrawal successful"
                return False, "Insufficient balance"
        return False, "Invalid account or PIN"

    @classmethod
    def update_user(cls, acc_no, pin, name=None, email=None, new_pin=None):
        data = cls.load_data()
        try:
            pin_value = cls._coerce_int(pin, "PIN")
        except ValueError as exc:
            return False, str(exc)

        for user in data:
            if user['accountNo.'] == acc_no and user['pin'] == pin_value:
                user['name'] = name or user['name']
                user['email'] = email or user['email']

                if new_pin not in (None, ""):
                    try:
                        new_pin_value = cls._coerce_int(new_pin, "New PIN")
                    except ValueError as exc:
                        return False, str(exc)
                    if len(str(abs(new_pin_value))) != 4:
                        return False, "New PIN should be 4 digits"
                    user['pin'] = new_pin_value

                cls.save_data(data)
                return True, "User details updated"
        return False, "User not found"

    @classmethod
    def delete_user(cls, acc_no, pin):
        data = cls.load_data()
        try:
            pin_value = cls._coerce_int(pin, "PIN")
        except ValueError as exc:
            return False, str(exc)

        for i, user in enumerate(data):
            if user['accountNo.'] == acc_no and user['pin'] == pin_value:
                data.pop(i)
                cls.save_data(data)
                return True, "Account deleted"
        return False, "Account not found"
