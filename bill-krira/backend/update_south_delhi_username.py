from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User

engine = create_engine('sqlite:///billing.db')
Session = sessionmaker(bind=engine)
session = Session()

def update_south_delhi_username():
    print("--- Updating South Delhi Username ---")
    user = session.query(User).filter_by(username='south-delhi').first()
    if user:
        print(f"Old Username: {user.username}")
        user.username = "sumit"
        # Also update the ID to keep it consistent if possible, 
        # but ID is primary key and might have foreign keys. 
        # Let's just update username for now as requested.
        session.commit()
        print(f"✅ New Username: {user.username}")
    else:
        print("❌ User 'south-delhi' not found.")

if __name__ == "__main__":
    update_south_delhi_username()
