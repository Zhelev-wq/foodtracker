"""
RUN ONLY ONCE TO CREATE DB TABLES
HAVE SEPARATE SOLUTION FOR MIGRATIONS
OR IDK
"""

from app.db import tables
from app.db.database import engine, Base
from sqlalchemy import text

def init_db():
    print("Creating database tables")
    Base.metadata.create_all(bind=engine)
    print("DB tables create or exist already")

    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        conn.commit()
if __name__ == "__main__":
    init_db()
