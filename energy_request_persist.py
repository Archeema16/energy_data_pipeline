from datetime import datetime
import json
import requests
from config import API_RETRY_COUNT, REPORTING_GROUPS
from utils import get_sql_connection, get_connection_cursor, close_db_access


def make_request(url, retry_count=0):
    """
    The function takes a URL and retrieves the API response. 
    In the event of a 5xx error or specific 4xx errors, the function retries up to API_RETRY_COUNT times.
    """
    data = {}
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()        
        return data
    except requests.exceptions.HTTPError as e:
        if 400 <= e.response.status_code < 500:
            error_data = e.response.json()
            data['error_note'] = error_data.get("errorNote")
            data['error_code'] = error_data.get("errorCode")
            if data['error_code'] in ["TimeOutException", "GeneralException"] and retry_count < API_RETRY_COUNT:
                retry_count += 1
                data = make_request(url,retry_count)
            return data
        elif 500 <= e.response.status_code < 600:
            data['error_code'] = e.response.status_code
            if retry_count < API_RETRY_COUNT:
                retry_count += 1
                data = make_request(url,retry_count)
            return data
        else:
            data['error_code'] = e.response.status_code
            return data
    except Exception as e:
        print(f"{datetime.now()} : Exception occured in API request :- {e}")
        return None   


def get_property_daily_energy_data(location_name, start_time, end_time, versiond_id="v1.0"):
    """
    The function takes a property location name, start time, and end time, then fetches daily energy consumption for all REPORTING_GROUPS in given range
    from the API and persists the data in the database. An optional version number can be specified, with the default being v1.0.
    """
    time_duration="Daily"
    version_id = versiond_id
    record = "LocationName"
    base_url = f"https://helsinki-openapi.nuuka.cloud/api/{version_id}/EnergyData/{time_duration}/ListByProperty"
    
    for reporting_group in REPORTING_GROUPS:
        url = f"{base_url}?Record={record}&SearchString={location_name}&ReportingGroup={reporting_group}&StartTime={start_time}&EndTime={end_time}"
        data = make_request(url)
        if not data is None:
            if 'error_code' in data:#Cater to both api error or HTTP error
                response = persist_error_api_response(data,location_name,start_time,end_time,versiond_id,reporting_group)
                if response:
                    print(f"{datetime.now()} : Error Data inserted for {location_name} , {reporting_group}")
            else:
                response = persist_api_response(data,versiond_id)
                if response:
                    print(f"{datetime.now()} : Data inserted successfully for {location_name} , {reporting_group}")
        else:
            print(f"{datetime.now()} : Breaking loop as excpetion occured")
            break 
   

def persist_error_api_response(data, location_name, start_time, end_time, versiond_id, reporting_group):
    insert_query = "INSERT INTO properties_daily_energy (location_name, reporting_group, date, response_error, version) VALUES (%s, %s, %s, %s, %s);"
    response_error = {}
    response_error["errorCode"] = data.get("error_code")
    response_error["errorNote"] = data.get("error_note")
    response_error["start_time"] = str(start_time) #As Date object is not serializable
    response_error["end_time"] = str(end_time)
    
    
    conn = get_sql_connection()
    if conn is None: return False
    cursor = get_connection_cursor(conn)
    if cursor is None: return False 
    
    try:
        values = (location_name, reporting_group, start_time, json.dumps(response_error), versiond_id)
        cursor.execute(insert_query,values)
        conn.commit()
        close_db_access(conn, cursor)
        return True
    except Exception as e:
        print(f"{datetime.now()} : Exception while inserting API Error Data: ", e)
        close_db_access(conn,cursor)
        return False
    

def persist_api_response(data, versiond_id):
    insert_query = "INSERT INTO properties_daily_energy (location_name, reporting_group, value, unit, date, version) VALUES (%s, %s, %s, %s, %s, %s);"
    
    conn = get_sql_connection()
    if conn is None: return False
    cursor = get_connection_cursor(conn)
    if cursor is None: return False 
    
    try:
        for daily_item in data:
            values = (daily_item.get("locationName"), daily_item.get("reportingGroup"), daily_item.get("value"), daily_item.get("unit"), daily_item.get("timestamp") , versiond_id)
            cursor.execute(insert_query,values)
        conn.commit()
        close_db_access(conn, cursor)
        return True
    except Exception as e:
        print(f"{datetime.now()} : Exception while inserting API Data: ", e)
        conn.rollback()
        close_db_access(conn, cursor)
        return False
