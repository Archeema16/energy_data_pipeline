from datetime import datetime, timedelta
from utils import create_table_if_not_exist, load_properties_json_in_db
from config import WEEK_INTERVAL, JSON_PROPERTIES_FILE_PATH

#ETL end date is 2 days ealrier as data in Open API is lagging 2 days behind. 
end_date = datetime.date(datetime.now()) - timedelta(days=2)
start_date = end_date -timedelta(weeks=WEEK_INTERVAL)
properties_list = ['1000 Hakaniemen kauppahalli','1001 Hietalahden kauppahalli','1002 Vanha kauppahalli','1037 Vuotalo','1507 Suutarilan monitoimitalo/ala-aste ja Lpk Seulanen']

#run script for creating table if not exists. 
tables_created = create_table_if_not_exist()
print(f"StartDate:- {start_date} , EndDate:- {end_date} , Tables Created If not existed:- {tables_created}")

if tables_created:
    #run script to read properties json file and load data into table
    data_loaded = load_properties_json_in_db(JSON_PROPERTIES_FILE_PATH)
    print(f"{datetime.now()} , Properties data loaded to table:- {data_loaded}")

else:
     print(f"{datetime.now()} , Pipeline Shutting down as unable to to create/access tables")