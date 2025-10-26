# python -m app.util.recreate_db   from root

from app.database import Base, engine
from app.models import user, habit  # import all models so they register with Base

if __name__ == "__main__":
    print("Dropping and recreating all tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Done.")