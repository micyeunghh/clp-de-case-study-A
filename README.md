# CLP Data Engineer Case Study A

## Part 1 - Setting up the database

To bootstrap a Postgres database in a docker container, [Docker Compose](https://github.com/docker/compose) was used with the docker-compose.yml file. It allows great flexibility on editing the docker configurations, including docker image used, database authentication, port number used and volumes attached to the container storing the actual data. The user could then spin up the postgres database in docker easily with just the ```docker-compose up``` command.

## Part 2 - Ingestion

A Flask application is created for this part of the requirements.

To allow user to upload the csv file, an HTML template was used in the root endpoint. The POST request was used to submit the file to the server and the pandas library was used to read and parse the csv file with sensor data.

To ingest the data into a Postgres database, the psycopg2 library was used for Postgres connection using Python. The database connection should use the same configurations (authentication, port etc.) in the docker-compose.yml file used to create the database in docker. To maintain the data characteristic requirements, temperature data will be divided by 100 and any errorneous humidity records would not be inserted into the database.

## Part 3 - Business Requirements
For handling the "dew point" requirement, I have used PySpark to perform the data transformation and aggregation in data-extraction.py. For simplicity, the script reads a csv file instead of reading from the data directly from the Postgres database.

As the "dew point" metric expects both temperature and relative humidity as inputs for individual sensor, the following assumptions have been made:

- Each ```sensor_id``` is associated with both temperature and humidity sensor.
- Both metrics would be collected at the same timestamp.
- For sensor receiving extreme humidity values, which are considered as 'errorneous records', on a specific timestamp, the dew point metrics would not be processed.

i.e. In reality, the data is expected to be similar to the [sample file](https://github.com/micyeunghh/clp-de-case-study-A/files/9712616/sample3.csv). The sample file provided should covered the handling of the following data characteristics:
- Negative humidity value
- Over-100 humidity value

