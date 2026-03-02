from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User

engine = create_engine('sqlite:///billing.db')
Session = sessionmaker(bind=engine)
session = Session()

def check_user():
    print("--- Checking User: south-delhi ---")
    user = session.query(User).filter_by(username='south-delhi').first()
    if user:
        print(f"Found User: {user.username}")
        print(f"Password: {user.password}")
        print(f"EmpCode: {user.empCode}")
        print(f"Region: {user.region}")
    else:
        print("❌ User 'south-delhi' NOT FOUND in database.")

    print("\n--- All Users ---")
    users = session.query(User).all()
    for u in users:
        print(f"User: {u.username} | Pass: {u.password} | Emp: {u.empCode}")

if __name__ == "__main__":
    check_user()
