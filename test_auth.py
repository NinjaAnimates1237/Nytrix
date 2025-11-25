import requests
import json

# Test the login flow
base_url = "http://localhost:6767/api"

# 1. Register a test user
print("Testing registration...")
try:
    response = requests.post(f"{base_url}/auth/register", json={
        "username": "testuser123",
        "email": "test123@example.com",
        "password": "TestPass123"
    })
    print(f"Register Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"Token received: {data['token'][:20]}...")
        token = data['token']
    else:
        print(f"Response: {response.text}")
        # Try login instead
        print("\nTrying login...")
        response = requests.post(f"{base_url}/auth/login", json={
            "email": "test123@example.com",
            "password": "TestPass123"
        })
        print(f"Login Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        token = data['token']

    # 2. Test /auth/me with the token
    print("\nTesting /auth/me...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{base_url}/auth/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"Error: {e}")
