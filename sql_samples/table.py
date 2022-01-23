from google.cloud.sql.connector import connector
from sql_samples.mapped_class import Address
from utils.db_connect import DB_CONNECTOR
from dotenv import dotenv_values
from sqlalchemy import text, MetaData, Table, Column, Integer, String, ForeignKey, insert, select, bindparam, func, cast, and_, or_
from sqlalchemy.orm import Session

config = dotenv_values("./.env")

cloud_sql_instance = config["CLOUD_SQL_INSTANCE"]
sql_username = config["SQL_USERNAME"]
sql_password = config["SQL_PASSWORD"]
sql_db_name = config["SQL_DB_NAME"]

db_connector = DB_CONNECTOR(cloud_sql_instance, sql_username, sql_password, sql_db_name)
_base_connector = connector.Connector()
engine = db_connector.init_connection_engine(_base_connector)

metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(30)),
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String(30), nullable=False),
)

metadata_obj.create_all(engine)

print(
    select(address_table).
    where(
        and_(
            or_(user_table.c.name == "akira", user_table.c.name == "sandy"),
            address_table.c.user_id == user_table.c.id
        )
    )
)