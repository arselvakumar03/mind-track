from fastapi import FastAPI

from app import models
from app.models.user import User
from app.routers import auth, userAccount

from app.database import SessionLocal, engine
from app.dependency import db_dependency as db_dependency
from app.security import hash_password   


app = FastAPI()

# include routers
app.include_router(auth.router)
app.include_router(userAccount.router)

#models.Base.metadata.create_all(bind=engine)
""" 
@app.on_event("startup")
def seed_admin_user():
    db = SessionLocal()
    try:
        # Check if any users exist
        if db.query(User).count() == 0:
            admin = User(
                username="admin",
                hashed_password=hash_password("password123"),  # default password
                email="admin@gmail.com"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print(f"Seeded initial admin user: {admin.username}")
    finally:
        db.close() 

"""