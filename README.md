# CLP Data Engineer Case Study A



## Part 3 - Business Requirements
For handling the "dew point" requirement, I have used PySpark to perform the data transformation and aggregation in data-extraction.py. For simplicity, the script reads a csv file instead of reading from the data directly from the Postgres database.

As the "dew point" metric expects both temperature and relative humidity as inputs for individual sensor, the following assumptions have been made:

- Each sensor_id is associated with both temperature and humidity sensor.
- Both metrics would be collected at the same timestamp.
- For sensor receiving extreme humidity values, which are considered as 'errorneous records', on a specific timestamp, the dew point metrics would not be processed.

i.e. In reality, the data is expected to be similar to the [sample file](https://github.com/micyeunghh/clp-de-case-study-A/files/9712616/sample3.csv). The sample file provided should covered the handling of the following data characteristics:
- Negative humidity value
- Over-100 humidity value

