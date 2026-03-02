from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User

engine = create_engine('sqlite:///billing.db')
Session = sessionmaker(bind=engine)
session = Session()

def fix_passwords():
    print("--- Fixing Passwords ---")
    users = session.query(User).filter(User.role != 'admin').all()
    
    count = 0
    for user in users:
        if user.username != 'krira-sumit': # Double check to skip admin
            print(f"Updating {user.username}...")
            user.password = "krira-sumit"
            count += 1
            
    session.commit()
    print(f"✅ Updated {count} users to password 'krira-sumit'")

if __name__ == "__main__":
    fix_passwords()
