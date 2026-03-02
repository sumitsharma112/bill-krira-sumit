import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"

# Default password for all users
DEFAULT_PASSWORD = "krira-sumit"

# List of users to create
# Format: (username, name, region, empCode)
USERS_TO_CREATE = [
    # Delhi Zones
    ("sumit", "South Delhi User", "Delhi", "krira-southdelhi"),
    ("east-delhi", "East Delhi User", "Delhi", "DL-E-01"),
    ("west-delhi", "West Delhi User", "Delhi", "DL-W-01"),
    ("central-delhi", "Central Delhi User", "Delhi", "DL-C-01"),
    
    # Haryana Cities
    ("faridabad", "Faridabad User", "Haryana", "HR-F-01"),
    ("rohtak", "Rohtak User", "Haryana", "HR-R-01"),
    ("gurgaon", "Gurgaon User", "Haryana", "HR-G-01"),
    
    # Other States
    ("rajasthan", "Rajasthan User", "Rajasthan", "RJ-01"),
    ("mp-user", "MP User", "Madhya Pradesh", "MP-01"),
    ("up-user", "UP User", "Uttar Pradesh", "UP-01"),
    
    # Main Admin (Updating if exists or creating)
    ("krira-sumit", "Sumit Admin", "all", "ADMIN-01")
]

def create_user(username, name, region, empCode):
    user_data = {
        "id": f"user-{username}",
        "username": username,
        "password": DEFAULT_PASSWORD,
        "role": "admin" if username == "krira-sumit" else "viewer", # Only sumit is admin
        "region": region,
        "name": name,
        "empCode": empCode
    }
    
    # First try to delete if exists (to update password/details)
    requests.delete(f"{BASE_URL}/users/user-{username}")
    
    # Create new
    res = requests.post(f"{BASE_URL}/users", json=user_data)
    if res.status_code == 200:
        print(f"✅ Created: {name} ({username}) - Code: {empCode}")
    else:
        print(f"❌ Failed {username}: {res.text}")

def main():
    print("--- Seeding Regional Users ---")
    print(f"Default Password: {DEFAULT_PASSWORD}\n")
    
    for username, name, region, empCode in USERS_TO_CREATE:
        create_user(username, name, region, empCode)
        
    print("\n--- Seeding Complete ---")

if __name__ == "__main__":
    main()
