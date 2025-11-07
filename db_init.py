"""
RUN ONLY ONCE TO CREATE DB TABLES
HAVE SEPARATE SOLUTION FOR MIGRATIONS
OR IDK
"""

from app.db import tables
from app.db.database import engine, Base


def init_db():
    print("Creating database tables")
    Base.metadata.create_all(bind=engine)
    print("DB tables create or exist already")


if __name__ == "__main__":
    init_db()
