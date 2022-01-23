from google.cloud.sql.connector import connector
from utils.db_connect import DB_CONNECTOR
from dotenv import dotenv_values
from sqlalchemy import text
from sqlalchemy.orm import Session

config = dotenv_values("./.env")

cloud_sql_instance = config["CLOUD_SQL_INSTANCE"]
sql_username = config["SQL_USERNAME"]
sql_password = config["SQL_PASSWORD"]
sql_db_name = config["SQL_DB_NAME"]

db_connector = DB_CONNECTOR(cloud_sql_instance, sql_username, sql_password, sql_db_name)
_base_connector = connector.Connector()
engine = db_connector.init_connection_engine(_base_connector)

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE IF NOT EXISTS some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 16}, {"x": 2, "y": 24}],
    )
    # conn.commit()

# with engine.connect() as conn:
#     result = conn.execute(text("SELECT x, y FROM some_table"))
#     for row in result:
#         print(f"x: {row.x} y: {row.y}")

# with engine.connect() as conn:
#     result = conn.execute(
#         text("SELECT x, y FROM some_table WHERE y > :y"),
#         {"y": 2},
#     )
#     for row in result:
#         print(f"x: {row.x} y: {row.y}")

with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{"x": 1, "y": 11}, {"x": 2, "y": 15}],
    )
    session.commit()

stmt= text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(y=6)
with Session(engine) as session:
    result = session.execute(stmt)
    for row in result:
        print(f"x: {row.x} y: {row.y}")