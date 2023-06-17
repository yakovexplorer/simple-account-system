import requests

base_url = "http://localhost:8000"

# Account creation endpoint
create_account_url = f"{base_url}/account/create/"

# Account deletion endpoint
delete_account_url = f"{base_url}/account/delete/"

# Account editing endpoint
edit_account_url = f"{base_url}/account/edit/"

# Login endpoint
login_url = f"{base_url}/account/login/"

# Account info endpoint
account_info_url = f"{base_url}/account/get/info/"

# Third-party API endpoint
third_party_api_url = "https://api.example.com"

# Create an account
def create_account(username, password, confirm_password, phone_number=None, email=None):
    data = {
        "username": username,
        "password": password,
        "confirm_password": confirm_password,
        "phone_number": phone_number,
        "email": email
    }
    response = requests.post(create_account_url, json=data)
    return response.json()

# Delete an account
def delete_account(username, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "username": username
    }
    response = requests.delete(delete_account_url, json=data, headers=headers)
    return response.json()

# Edit an account
def edit_account(username, token, phone_number=None, email=None):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "username": username,
        "phone_number": phone_number,
        "email": email
    }
    response = requests.put(edit_account_url, json=data, headers=headers)
    return response.json()

# Login and obtain an access token
def login(username, password):
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(login_url, json=data)
    return response.json()

# Get account info
def get_account_info(username, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "username": username
    }
    response = requests.post(account_info_url, json=data, headers=headers)
    return response.json()

# Access third-party API (requires login)
def access_third_party_api(username, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(third_party_api_url, headers=headers)
    return response.json()

# Prompt for user input
def prompt_user():
    print("Select an option:")
    print("1. Create an account")
    print("2. Login")
    print("3. Get account info")
    print("4. Delete an account")
    print("5. Edit an account")
    print("6. Access third-party API")
    option = input("Enter option number: ")

    if option == "1":
        username = input("Enter username: ")
        password = input("Enter password: ")
        confirm_password = input("Confirm password: ")
        phone_number = input("Enter phone number (optional): ")
        email = input("Enter email (optional): ")
        account = create_account(username, password, confirm_password, phone_number, email)
        print(account)
    elif option == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")
        login_response = login(username, password)
        print(login_response)
        if "access_token" in login_response:
            access_token = login_response["access_token"]
            info = get_account_info(username, access_token)
            print(info)
    elif option == "3":
        username = input("Enter username: ")
        access_token = input("Enter access token: ")
        info = get_account_info(username, access_token)
        print(info)
    elif option == "4":
        username = input("Enter username: ")
        access_token = input("Enter access token: ")
        account = delete_account(username, access_token)
        print(account)
    elif option == "5":
        username = input("Enter username: ")
        access_token = input("Enter access token: ")
        phone_number = input("Enter new phone number (optional): ")
        email = input("Enter new email (optional): ")
        account = edit_account(username, access_token, phone_number, email)
        print(account)
    elif option == "6":
        username = input("Enter username: ")
        access_token = input("Enter access token: ")
        third_party_response = access_third_party_api(username, access_token)
        print(third_party_response)
    else:
        print("Invalid option. Please try again.")

# Prompt the user for input
prompt_user()
