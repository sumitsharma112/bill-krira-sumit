from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User

engine = create_engine('sqlite:///billing.db')
Session = sessionmaker(bind=engine)
session = Session()

def update_south_delhi_code():
    print("--- Updating South Delhi Emp Code ---")
    user = session.query(User).filter_by(username='south-delhi').first()
    if user:
        print(f"Old Code: {user.empCode}")
        user.empCode = "krira-southdelhi"
        session.commit()
        print(f"✅ New Code: {user.empCode}")
    else:
        print("❌ User 'south-delhi' not found.")

if __name__ == "__main__":
    update_south_delhi_code()
