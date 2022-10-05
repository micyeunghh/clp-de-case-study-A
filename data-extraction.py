from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, TimestampType, StringType
from pyspark.sql.functions import col, when, window, avg

# Initiate a Spark session
spark = SparkSession \
    .builder \
    .appName("Sensor Data Extraction") \
    .getOrCreate()

filepath = './sample3.csv'

# Read a CSV File
df = spark.read.option("header", True).csv(filepath)

# Change columns to appropriate data types
df = df.withColumn("timestamp", df['timestamp'].cast(TimestampType()))
df = df.withColumn("reading", df['reading'].cast(IntegerType()))

# Create a column for normal-scaled temperature
df = df.withColumn('norm_reading', when(df.sensor_type == 'temperature', df.reading/100).otherwise(df.reading))

# Remove extreme humidity values 
df = df.filter(~((df.sensor_type == 'humidity') & ((df.norm_reading < 0) | (df.norm_reading > 100))))

# Pivot the data on sensor type
df = df.groupBy('sensor_id', 'timestamp').pivot('sensor_type').sum('norm_reading').orderBy('sensor_id', 'timestamp')

# Create a column for dew point metric
df = df.withColumn('dew_point', (100 - 5*df.temperature - df.humidity/100)/5)

# Create a 30-min time interval column and group the data by this column
df = df.groupBy('sensor_id', window('timestamp', '30 minutes').alias('time_interval')).agg(avg('dew_point').alias('avg_dew_point')).orderBy('sensor_id', 'time_interval')

# Clean the null dew point values expected from extreme humidity values
df = df.filter((df.avg_dew_point.isNotNull()))

# Change the time interval column to string for output
df = df.withColumn('time_interval', col('time_interval').cast(StringType()))

# Export the data to a new CSV file
df.write.option("header",True).csv("./pyspark_out/")
