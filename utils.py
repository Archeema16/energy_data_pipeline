from datetime import datetime
import json
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
        # DateTime is added to logs for improved readability and easier debugging
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
        print(f"{datetime.now()} : Unable to Close Connection and Cursor , Exception: ",e)
    
def close_db_connection(conn):
    try:
        conn.close()
    except Exception as e:
        print(f"{datetime.now()} : Unable to close Connection , Exception: ",e)

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
        print(f"{datetime.now()} : Tables Schema created successfully!")
        close_db_access(conn,cursor)
        return True
    except Exception as e:
        print(f"{datetime.now()} : Error while creating tables:", e)
        close_db_access(conn,cursor)
        return False

def load_properties_json_in_db(json_filepath):
    """
    Loads properties from a JSON file into the database.
    This function is parameterized to accommodate future use cases where different properties JSON files might need to be processed.
    """
    # SQL parameterized query for inserting data
    insert_query = "INSERT INTO properties (location_name, property_name, property_code) VALUES (%s, %s, %s); "

    conn = get_sql_connection()
    if conn is None: return False
    cursor = get_connection_cursor(conn)
    if cursor is None: return False 
    
    try:
        
        # UTF-8 encoding is taken as special character are present in JSON file
        with open(json_filepath,'r',encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        # Iterate over JSON data and insert each item
        for item in data:
            cursor.execute(insert_query, (
                item.get('locationName'),
                item.get('propertyName'),
                item.get('propertyCode'))
            )
        
        conn.commit()
        print(f"{datetime.now()} : Data inserted successfully!")
        close_db_access(conn, cursor)
        return True
    except Exception as e:
        print(f"{datetime.now()} : Error inserting data:", e)
        conn.rollback()  # Rollback in case of error
        close_db_access(conn, cursor)
        return False