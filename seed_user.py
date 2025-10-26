
from app.database import SessionLocal
from app.models.user import User
from app.security import hash_password

# open a session
db = SessionLocal()

try:
    # create a new user
    user = User(
        username="selva",
        hashed_password=hash_password("password123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Created user: {user.id} - {user.username}")
finally:
    db.close()