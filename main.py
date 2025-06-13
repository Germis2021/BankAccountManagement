# # You will create a fastapi application for Bank Account Managament.

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



# a fastapi system for account managament

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Account(BaseModel):
    id: int
    type: str
    person_name: str
    address: str

# type hint for a list of accounts
accounts:list[Account] = []

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
