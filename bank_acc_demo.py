# 1dalis
#  # You will create a fastapi application for Bank Account Managament.

# 1. Create a Github repo for this project.
# 2. Create a separate folder for project.
# 3. Create a fastapi application where can do CRUD (no need for update).
# 4. Demonstrate that u are able to Create, read and Delete the account.
# 5. Account should have 
#  - id, 
#  - type (which can be either 'business' or 'personal', it can be a string for now)
#  - person_name
#  - address.

# ---------------------------------------------------

# 2dalis

# The product owner has requested additional functionality to be able to create payments:

# 1. Payment resource will have:
#  - id: int
#  - from_account_id: int (account id from which we are sending from)
#  - to_account_id: int (account id from which we are sending to)
#  - amount_in_euros: int
#  - payment_date: date

# 2. Create this resource and add create, get_all, get_by_id methods.

# Optional, advanced
# - Please check if the accounts are valid and the sum is more than 0, if not return 400.

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Account(BaseModel):
    id: int
    type: str
    person_name: str
    address: str

class Payment(BaseModel):
    id: int
    from_account_id: int
    to_account_id: int
    amount_in_euros: float
    payment_date: str  # Using string for date, can be improved with datetime    

# type hint for a list of accounts
accounts:list[Account] = []

payments:list[Payment] = []

@app.post("/accounts/")
def create_account(account: Account):
    accounts.append(account)
    return {"message": "Account created successfully"}

@app.get("/accounts/")
def get_accounts():
    return accounts

@app.get("/accounts/{account_id}")
def get_account(account_id: int):
    for account in accounts:
        if account.id == account_id:
            return account
    return {"message": "Account not found"}

@app.delete("/accounts/{account_id}")
def delete_account(account_id: int):
    accounts[:] = [account for account in accounts if account.id != account_id]
    return {"message": "Account deleted successfully"}



@app.post("/payments/")
def create_payment(payment: Payment):
    # Check if accounts are valid
    from_account = next((acc for acc in accounts if acc.id == payment.from_account_id), None)
    to_account = next((acc for acc in accounts if acc.id == payment.to_account_id), None)
    
    if not from_account or not to_account:
        return {"message": "Invalid account(s)"}, 400
    
    if payment.amount_in_euros <= 0:
        return {"message": "Amount must be greater than 0"}, 400
    
    payments.append(payment)
    return {"message": "Payment created successfully"}

@app.get("/payments/")
def get_payments():
    return payments

@app.get("/payments/{payment_id}")
def get_payment(payment_id: int):
    for payment in payments:
        if payment.id == payment_id:
            return payment
    return {"message": "Payment not found"}