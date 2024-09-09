# energy_data_pipeline
This repository contains code to connect to a local PostgreSQL database and process a JSON file listing service properties in the city of Helsinki. The code selects five properties from the JSON data and retrieves their energy consumption details from the [Nuuka Open API](https://helsinki-openapi.nuuka.cloud/swagger/index.html#/).<br><br>

**Setup**:- <br>
- To create the setup,  branch was created from main using git command "git checkout -b initial_setup_branch" <br>
- To create a local PostgreSQL database docker conatiner is used with latest image of postgres.<br>
- To interact with the database using python install psycopg2 library in your environemnt. <br>
- The configuration required to connect to local PostgreSQL database are present in config.py . The configuration however donot have secrets present in it as it is best practice to not commit credentials to git repository.  Incase you decide to make your own local postgres database , do change the config settings accordingly. <br>
- The file provided in the assignment is also being committed here and its path is provided in the config.py. The path can be changed to run the code locally. <br>
- Git commands used in this branch are git branch , git status , git add . , git reset , git commit -m "" , git push origin initial_setup_branch <br>

**Task 2.3**:- <br>
- Properties energy table is created with following understanding and future purposes :- <br>
    After evaluating the API endpoint and the provided property file, location_name was selected as the key identifier for retrieving data. While property_code may be similar across multiple locations, it remains consistent for the same location_name. <br>
    location_name: This field is not set as a foreign key because it is not unique across all records of properties table.<br>
    load_date: This field tracks when a particular record was loaded through the ETL process. <br>
    version_id: This field keeps track of which version of the API was used to receive the data. It is essential for ensuring data consistency and accommodating future updates. <br>
    response_error: This field stores any errors encountered during API calls in JSON format. This allows for easier investigation in the future and enables the creation of ETL workflows to address failed retrievals. <br>
    Indexes have been created to improve query performance, as the table is expected to grow significantly in size over time. <br>
- Due to limited api documentation and a failed proof of concept, only one reporting group is processed per API call. <br>
- A single API call retrieves data for the entire date range for one reporting group and property at a time. <br>
- All 4 reporting groups are configured in config.py. The code is designed to accommodate future changes in the reporting groups, allowing for additions or removals by simply updating the configuration file. <br>
- The API retry mechanism is also configurable via the config.py file and can be adjusted as needed. <br>
- The retry logic has been implemented for both 5xx errors and specific 4xx errors (GeneralException, TimeOutException), based on the API documentation.<br>
- Git commands used in this branch are similar to Setup branch <br>

**Task 2.4**:- <br>
- Combined the data from the two tables, properties and properties_daily_energy, by using location_name as the join key. This ensures that the energy usage data from the properties_daily_energy table is correctly linked to the corresponding properties in the properties table. <br>
    Optimized the query by joining the smaller table (properties) first, reducing the amount of data processed when joining it with the larger table (properties_daily_energy).<br>
    To ensure data quality, filtered out any records where response_error is not null, as these entries likely indicate unsuccessful API calls. <br>
    Further, grouped the data by location_name, reporting_group, and unit. This grouping allowed to aggregate the energy usage for each property and its respective reporting group.<br>
    The aggregation is done by summing the value field to calculate the total energy consumption per reporting group. Additionally, counted the number of rows in each group to determine the total number of days for which we have data. <br>
    To improve readability, ordered the result set in ascending order by location_name. <br>
- Added sample queries and a general lookup function (fetch_data_db) for ease of data retrieval.
- Git commands used in this branch git fetch origin, git checkout, git switch, and other similar to Setup branch <br><br>

**Sample Output**:- <br>
2024-09-10 00:13:16.017841 : Tables Schema created successfully!
StartDate:- 2024-08-25 , EndDate:- 2024-09-08 , Tables Created If not existed:- True
2024-09-10 00:13:16.555517 : Data inserted successfully!
2024-09-10 00:13:16.556054 , Properties data loaded to table:- True
2024-09-10 00:13:17.268566 : Data inserted successfully for 1000 Hakaniemen kauppahalli , Electricity
2024-09-10 00:13:17.973388 : Data inserted successfully for 1000 Hakaniemen kauppahalli , Heat
2024-09-10 00:13:18.684646 : Error Data inserted for 1000 Hakaniemen kauppahalli , Water
2024-09-10 00:13:19.335392 : Error Data inserted for 1000 Hakaniemen kauppahalli , DistrictCooling
2024-09-10 00:13:20.142624 : Data inserted successfully for 1001 Hietalahden kauppahalli , Electricity
2024-09-10 00:13:20.771434 : Data inserted successfully for 1001 Hietalahden kauppahalli , Heat
2024-09-10 00:13:21.442659 : Error Data inserted for 1001 Hietalahden kauppahalli , Water
2024-09-10 00:13:22.118862 : Error Data inserted for 1001 Hietalahden kauppahalli , DistrictCooling
2024-09-10 00:13:22.791449 : Data inserted successfully for 1002 Vanha kauppahalli , Electricity
2024-09-10 00:13:23.450660 : Data inserted successfully for 1002 Vanha kauppahalli , Heat
2024-09-10 00:13:24.087885 : Error Data inserted for 1002 Vanha kauppahalli , Water
2024-09-10 00:13:24.691321 : Error Data inserted for 1002 Vanha kauppahalli , DistrictCooling
2024-09-10 00:13:25.351757 : Data inserted successfully for 1037 Vuotalo , Electricity
2024-09-10 00:13:25.980865 : Data inserted successfully for 1037 Vuotalo , Heat
2024-09-10 00:13:26.603135 : Data inserted successfully for 1037 Vuotalo , Water
2024-09-10 00:13:27.221306 : Error Data inserted for 1037 Vuotalo , DistrictCooling
2024-09-10 00:13:27.859908 : Data inserted successfully for 1507 Suutarilan monitoimitalo/ala-aste ja Lpk Seulanen , Electricity
2024-09-10 00:13:28.558374 : Data inserted successfully for 1507 Suutarilan monitoimitalo/ala-aste ja Lpk Seulanen , Heat
2024-09-10 00:13:29.163743 : Error Data inserted for 1507 Suutarilan monitoimitalo/ala-aste ja Lpk Seulanen , Water
2024-09-10 00:13:29.875656 : Error Data inserted for 1507 Suutarilan monitoimitalo/ala-aste ja Lpk Seulanen , DistrictCooling
2024-09-10 00:13:29.897797 : Properties Energy Stats as follows:-
('1000 Hakaniemen kauppahalli', 'Electricity', 454.44, 'kWh', 14)
('1000 Hakaniemen kauppahalli', 'Heat', 8306.0, 'kWh', 14)
('1001 Hietalahden kauppahalli', 'Electricity', 15129.066999999997, 'kWh', 15)
('1001 Hietalahden kauppahalli', 'Heat', 4976.0, 'kWh', 14)
('1002 Vanha kauppahalli', 'Electricity', 4638.759999999999, 'kWh', 14)
('1002 Vanha kauppahalli', 'Heat', 8991.0, 'kWh', 14)
('1037 Vuotalo', 'Electricity', 31007.26, 'kWh', 15)
('1037 Vuotalo', 'Heat', 3912.0, 'kWh', 15)
('1037 Vuotalo', 'Water', 1644.0, 'M3', 15)
('1507 Suutarilan monitoimitalo/ala-aste ja Lpk Seulanen', 'Electricity', 28397.710000000003, 'kWh', 15)
('1507 Suutarilan monitoimitalo/ala-aste ja Lpk Seulanen', 'Heat', 4809.0, 'kWh', 14)

**Disclaimer** :- The Properties Energy Stats will change according to the time ETL ran.