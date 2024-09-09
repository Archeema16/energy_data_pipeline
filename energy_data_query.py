from datetime import datetime
from utils import get_sql_connection, get_connection_cursor

#Sample Queries
query1 = "select * from properties"
query2 = "select * from properties_daily_energy"
query3 = "select distinct(response_error->'errorCode')  from properties_daily_energy where response_error is not null"


def fetch_display_energy_data_stats():
    query = """select p.location_name , reporting_group , sum(value) as total_usage, unit, count(*) as number_of_days from properties p join properties_daily_energy pe
                on pe.location_name = p.location_name
                where response_error is null
                group by p.location_name , reporting_group, unit
                order by p.location_name"""
    
    conn = get_sql_connection()
    cursor = get_connection_cursor(conn)

    if conn is None or cursor is None:
        print(f"{datetime.now()} : Cannot access Database currently.")

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f"{datetime.now()} : Properties Energy Stats as follows:- ")
        for row in rows:
            print(row)
    except Exception as e:
        print(f"{datetime.now()} : Exception occured while fetching energy data stats.", e)




def fetch_data_db(query):
    """
    The function is designed for quickly retrieving data from the database based on a provided query.
    """
    conn = get_sql_connection()
    cursor = get_connection_cursor(conn)

    if conn is None or cursor is None:
        print(f"{datetime.now()} : Cannot access Database currently.")
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(f"{datetime.now()} : Exception occured while fetching data from database.", e)