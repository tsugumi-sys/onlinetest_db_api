import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import connector
import pymysql
from dotenv import dotenv_values


config = dotenv_values("./.env")

cloud_sql_instance = config["CLOUD_SQL_INSTANCE"]
sql_username = config["SQL_USERNAME"]
sql_password = config["SQL_PASSWORD"]
sql_db_name = config["SQL_DB_NAME"]

class SQL_CONNECTOR:
    def __init__(self, cloud_sql_instance: str, sql_username: str, sql_password:str, sql_db_name: str) -> None:
        self.cloud_sql_instance = cloud_sql_instance
        self.user_name = sql_username
        self.password = sql_password
        self.db_name = sql_db_name
    
    def init_connection_engine(
        self,
    ) -> sqlalchemy.engine.Engine:
        def getconn() -> pymysql.connections.Connection:
            conn: pymysql.connections.Connection = connector.connect(
                self.cloud_sql_instance,
                "pymysql",
                user=self.user_name,
                password=self.password,
                db=self.db_name,
            )
            return conn

        engine = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=getconn,
        )
        return engine

engine = SQL_CONNECTOR(cloud_sql_instance, sql_username, sql_password, sql_db_name).init_connection_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()