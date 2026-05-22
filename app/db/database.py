from dotenv import dotenv_values
from sqlalchemy import Column, MetaData, Table, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

config = dotenv_values("./app/.env")
db = config.get("DB")
username = config.get("USERNAME")
password = config.get("PASSWORD")
host_address = config.get("HOST_ADDRESS")
port = config.get("PORT")


engine = create_engine(
    f"{db}://{username}:{password}@{host_address}:{port}/food", echo=True
)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    with SessionLocal() as db:
        yield db
