# energy_data_pipeline
This repository contains code to connect to a local PostgreSQL database and process a JSON file listing service properties in the city of Helsinki. The code selects five properties from the JSON data and retrieves their energy consumption details from the [Nuuka Open API](https://helsinki-openapi.nuuka.cloud/swagger/index.html#/).<br><br>

**Setup**:- <br>
- To create the setup,  branch was created from main using git command "git checkout -b initial_setup_branch" <br>
- To create a local PostgreSQL database docker conatiner is used with latest image of postgres.<br>
- To interact with the database using python install psycopg2 library in your environemnt. 
- The configuration required to connect to local PostgreSQL database are present in config.py . The configuration however donot have secrets present in it as it is best practice to not commit credentials to git repository.  Incase you decide to make your own local postgres database , do change the config settings accordingly. <br>
- 
