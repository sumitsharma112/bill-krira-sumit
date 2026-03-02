from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User

engine = create_engine('sqlite:///billing.db')
Session = sessionmaker(bind=engine)
session = Session()

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
    
    # Main Admin
    ("krira-sumit", "Sumit Admin", "all", "ADMIN-01")
]

def seed_users():
    print("--- Seeding Users Directly ---")
    for username, name, region, empCode in USERS_TO_CREATE:
        # Check if user exists
        user = session.query(User).filter_by(username=username).first()
        password = "Ankit-Sumit" if username == "krira-sumit" else "krira-sumit"
        
        if user:
            print(f"Updating {username}...")
            user.name = name
            user.region = region
            user.empCode = empCode
            user.password = password
        else:
            print(f"Creating {username}...")
            new_user = User(
                id=f"user-{username}",
                username=username,
                password=password,
                role="admin" if username == "krira-sumit" else "user",
                name=name,
                region=region,
                empCode=empCode
            )
            session.add(new_user)
    
    session.commit()
    print("✅ Seeding complete.")

if __name__ == "__main__":
    seed_users()
