from google.cloud.sql.connector import connector
import pymysql
import sqlalchemy


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