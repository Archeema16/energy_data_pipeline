from datetime import datetime
import psycopg2
from config import POSTGRES_DB_NAME,POSTGRES_USER,POSTGRES_PASSWORD,POSTGRES_PORT,POSTGRES_HOST,SQL_FILE_PATH

def get_sql_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DB_NAME,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
    except Exception as e:
        print(f"{datetime.now()} : Unable to get Connection , Exception: ",e)
    return conn

def get_connection_cursor(conn):
    cursor = None
    try:
        cursor = conn.cursor()
    except Exception as e:
        print(f"{datetime.now()} : Unable to get Connection Cursor , Exception: ",e)
    return cursor

def close_db_access(conn,cursor):
    try:
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"{datetime.now()} : Unable to get Connection Cursor , Exception: ",e)
    
def close_db_connection(conn):
    try:
        conn.close()
    except Exception as e:
        print(f"{datetime.now()} : Unable to get Connection Cursor , Exception: ",e)

def create_table_if_not_exist():

    conn = get_sql_connection()
    if conn is None: return False
    cursor = get_connection_cursor(conn)
    if cursor is None: return False 

    try:
        with open(SQL_FILE_PATH, 'r') as file:
            sql_file = file.read()
        cursor.execute(sql_file)
        conn.commit()
        print(f"{datetime.now()} : Table Schema created successfully!")
        close_db_access(conn,cursor)
        return True
    except Exception as e:
        print(f"{datetime.now()} : Error while creating table:", e)
        return False
