import unittest
from google.cloud.sql.connector import connector
from dotenv import dotenv_values
import pymysql
import sqlalchemy
import logging

logger = logging.getLogger(__file__)


class DB_CONNECTOR:
    def __init__(self, cloud_sql_instance: str, sql_username: str, sql_password:str, sql_db_name: str) -> None:
        self.cloud_sql_instance = cloud_sql_instance
        self.user_name = sql_username
        self.password = sql_password
        self.db_name = sql_db_name
    
    def init_connection_engine(
        self,
        custom_connector: connector.Connector,
    ) -> sqlalchemy.engine.Engine:
        def getconn() -> pymysql.connections.Connection:
            conn: pymysql.connections.Connection = custom_connector.connect(
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

    def test_connector(self) -> None:
        _connector = connector.Connector()

        try:
            pool = self.init_connection_engine(_connector)

            with pool.connect() as conn:
                conn.execute("SELECT 1")
        
        except Exception as e:
            logger.exception("Failed to connect.", e)


class DB_CONNECT_TEST(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        config = dotenv_values("./.env")
        self.cloud_sql_instance = config["CLOUD_SQL_INSTANCE"]
        self.sql_username = config["SQL_USERNAME"]
        self.sql_password = config["SQL_PASSWORD"]
        self.sql_db_name = config["SQL_DB_NAME"]
    
    def test_connector(self) -> None:
        db_connector = DB_CONNECTOR(self.cloud_sql_instance, self.sql_username, self.sql_password, self.sql_db_name)

        with self.assertRaises(Exception):
            db_connector.test_connector()


if __name__ == "__main__":
    unittest.main()