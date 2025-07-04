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

# 3 dalis

#Please create an endpoint for reporting.

#This report should return a list of all transactions in the following format in json:
#  - from_person_name
#  - to_person_name
#  - amount_in_euros
#  - payment

#This endpoint should return an array of jsons with the information above.
#The endpoint should be GET /report 

from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.responses import FileResponse
import json


app = FastAPI()

class Account(BaseModel):
    id: int
    type: str
    person_name: str
    address: str

# Account file operations

def write_account_to_file(accounts: Account):
    with open("accounts.txt", "a") as file:
        file.write(f"{accounts.id}, {accounts.type}, {accounts.person_name}, {accounts.address}\n")

def read_accounts_from_file():
    accounts = []
    with open("accounts.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 10:
                id, type, person_name, address = parts
                accounts.append(Account(id=int(id), type=type.strip(), person_name=person_name.strip(), address=address.strip()))
    return accounts


            
class Payment(BaseModel):
    id: int
    from_account_id: int
    to_account_id: int
    amount_in_euros: int
    payment_date: str  
    
def write_payment_to_file(payments: Payment):
    with open("payments.txt", "a") as file:
        file.write(f"{payments.id}, {payments.from_account_id}, {payments.to_account_id}, {payments.amount_in_euros}, {payments.payment_date}\n")
    
def read_payments_from_file():
    payments = []
    with open("payments.txt", "r") as file:
        for line in file:
            id, from_account_id, to_account_id, amount, date = line.strip().split(",")
            payments.append(Payment(
                id=int(id),
                from_account_id=int(from_account_id),
                to_account_id=int(to_account_id),
                amount_in_euros=float(amount),
                payment_date=date
            ))
    return payments

class ReportRow(BaseModel):
    from_person_name: str
    to_person_name: str
    amount_in_euros: float
    payment_date: str 



def report():
    
    report = []
    accounts = read_accounts_from_file()
    payments = read_payments_from_file()
    
    for payment in payments:
        from_account = next((acc for acc in accounts if acc.id == payment.from_account_id), None)
        to_account = next((acc for acc in accounts if acc.id == payment.to_account_id), None)

        if from_account and to_account:
            report.append({
                "from_person_name": from_account.person_name,
                "to_person_name": to_account.person_name,
                "amount_in_euros": payment.amount_in_euros,
                "payment_date": payment.payment_date
            })

    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False) 

    return report













# type hint for a list of accounts
accounts:list[Account] = read_accounts_from_file()

payments:list[Payment] = read_payments_from_file()





@app.post("/accounts/")
def create_account(account: Account):
   
    write_account_to_file(account)
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
    write_payment_to_file(payment)
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

@app.get("/report/")
def get_report_json():
    return report()




