from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy import text
from dotenv import dotenv_values

config = dotenv_values(".env")
db = config.get("DB")
username = config.get("USERNAME")
password = config.get("PASSWORD")
host_address = config.get("HOST_ADDRESS")
port = config.get("PORT")


engine = create_engine(
    f"{db}://{username}:{password}@{host_address}:{port}/food", echo=True
)
with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())
