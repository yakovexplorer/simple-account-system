from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.hash import bcrypt
import json
import secrets
from typing import Optional

app = FastAPI(title="Account system V2")
database = []

# Model for account creation
class AccountCreate(BaseModel):
    username: str
    password: str
    phone_number: Optional[str]
    email: Optional[str]

# Model for account login
class AccountLogin(BaseModel):
    username: str
    password: str

# Model for account info
class AccountInfo(BaseModel):
    username: str

# Model for login response
class LoginResponse(BaseModel):
    access_token: str

# Create a new account
@app.post("/account/create/")
def create_account(account: AccountCreate):
    username = account.username
    password = bcrypt.hash(account.password)
    phone_number = account.phone_number
    email = account.email
    
    # Check if username already exists
    for entry in database:
        if entry["username"] == username:
            raise HTTPException(status_code=400, detail="Username already exists")

    new_account = {
        "username": username,
        "password": password,
        "phone_number": phone_number,
        "email": email
    }
    database.append(new_account)
    save_accounts()
    return {"message": "Account created successfully"}

# Delete an account
@app.delete("/account/delete/")
def delete_account(account: AccountInfo):
    username = account.username

    # Check if username exists
    for entry in database:
        if entry["username"] == username:
            database.remove(entry)
            save_accounts()
            return {"message": "Account deleted successfully"}

    raise HTTPException(status_code=404, detail="Account not found")

# Edit an account
@app.put("/account/edit/")
def edit_account(account: AccountInfo, phone_number: Optional[str] = None, email: Optional[str] = None):
    username = account.username

    # Check if username exists
    for entry in database:
        if entry["username"] == username:
            if phone_number is not None:
                entry["phone_number"] = phone_number
            if email is not None:
                entry["email"] = email
            save_accounts()
            return {"message": "Account updated successfully"}

    raise HTTPException(status_code=404, detail="Account not found")

# Login
@app.post("/account/login/")
def login(account: AccountLogin):
    username = account.username
    password = account.password

    # Check if username exists
    for entry in database:
        if entry["username"] == username:
            if bcrypt.verify(password, entry["password"]):
                token = generate_token()
                entry["token"] = token
                save_accounts()
                return LoginResponse(access_token=token)
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")

    raise HTTPException(status_code=404, detail="Account not found")

# Get detailed account info
@app.post("/account/get/info/")
def get_account_info(account: AccountInfo):
    username = account.username

    # Check if username exists
    for entry in database:
        if entry["username"] == username:
            account_info = {"username": entry["username"]}
            return account_info

    raise HTTPException(status_code=404, detail="Account not found")

# Generate a random access token
def generate_token():
    return secrets.token_hex(16)

# Load accounts from JSON file
def load_accounts():
    try:
        with open("accounts.json", "r") as file:
            global database
            database = json.load(file)
    except FileNotFoundError:
        pass

# Save accounts to JSON file
def save_accounts():
    with open("accounts.json", "w") as file:
        json.dump(database, file)

# Load accounts when the server starts
load_accounts()
