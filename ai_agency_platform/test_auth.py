import requests
import time

AUTH_URL = "http://localhost:8001/api/v1"
USERNAME = "user@example.com"
PASSWORD = "password"

# 1. Login
def login():
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    print(f"Attempting login as {USERNAME}...")
    response = requests.post(f"{AUTH_URL}/login/access-token", data=login_data)
    return response

try:
    response = login()
    
    # If login fails, try to signup
    if response.status_code != 200:
        print("Login failed, attempting signup...")
        signup_data = {
            "email": USERNAME,
            "password": PASSWORD,
            "full_name": "Test User",
            "is_superuser": True
        }
        signup_res = requests.post(f"{AUTH_URL}/signup", json=signup_data)
        if signup_res.status_code == 200:
            print("Signup successful! Logging in...")
            response = login()
        else:
            print(f"Signup failed: {signup_res.status_code} {signup_res.text}")
            exit(1)

    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"Login successful. Token: {token[:10]}...")
        
        # 2. Test /users/me
        headers = {"Authorization": f"Bearer {token}"}
        print("Testing /users/me...")
        me_response = requests.get(f"{AUTH_URL}/users/me", headers=headers)
        
        if me_response.status_code == 200:
            print("Success! User details:", me_response.json())
        else:
            print(f"Failed /users/me: {me_response.status_code} {me_response.text}")
            
    else:
        print(f"Login failed: {response.status_code} {response.text}")

except Exception as e:
    print(f"Error: {e}")
