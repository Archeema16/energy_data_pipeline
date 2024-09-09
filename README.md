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
- 

