from google.cloud.sql.connector import connector
from utils.db_connect import DB_CONNECTOR
from dotenv import dotenv_values
from sqlalchemy import text, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base

config = dotenv_values("./.env")

cloud_sql_instance = config["CLOUD_SQL_INSTANCE"]
sql_username = config["SQL_USERNAME"]
sql_password = config["SQL_PASSWORD"]
sql_db_name = config["SQL_DB_NAME"]

db_connector = DB_CONNECTOR(cloud_sql_instance, sql_username, sql_password, sql_db_name)
_base_connector = connector.Connector()
engine = db_connector.init_connection_engine(_base_connector)

Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("user_account.id"))

    user = relationship("User", back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id}, email_address={self.email_address})"


sandy = User(name="sandy", fullname="Sandy Cheeks")
print(sandy)