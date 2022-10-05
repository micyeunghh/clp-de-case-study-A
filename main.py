from sqlite3 import Cursor, Timestamp
from tkinter import INSERT
from flask import Flask, jsonify, request, render_template, redirect, url_for
import psycopg2
import os
import pandas as pd

app = Flask(__name__)

### Configs ###

# Config - File Upload
UPLOAD_FOLDER = './uploaded'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Config - PostgresSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres",
    port='5438')

cur = conn.cursor()

# SQL statement for inserting records
sql = '''INSERT INTO sensors
        VALUES(%s, %s, %s, %s);'''

# Adding sensor record to the Postgres database table
def addSensor(id, t, st, r):
    cur.execute (sql, (id, t, st, r))
    conn.commit()

# Read the CSV file imported by users
def parseCSV(filePath):
    # Use Pandas to parse the CSV file
    df = pd.read_csv(filePath, header=0)

    # Change column to appropriate data type
    df['reading'] = df['reading'].astype(float)

    # Loop through the rows and insert the sensor records into the database
    for i, row in df.iterrows():
        # Condition check - if it is temperature reading, divide by 100
        if row['sensor_type'] == 'temperature':
            addSensor(row['sensor_id'],row['timestamp'],row['sensor_type'],(row['reading'])/100)
        # Condition check - extreme humidity reading
        elif row['reading'] > 0 and row['reading'] < 100:
            addSensor(row['sensor_id'],row['timestamp'],row['sensor_type'],(row['reading']))

# HTML layout for user to upload CSV files
@app.route('/')
def index():
    return render_template('index.html')

# User to upload the CSV files
@app.route("/", methods=['POST'])
def uploadFiles():
      # Get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
        # Set the file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # Save the file
        uploaded_file.save(file_path)
        # Read CSV file and insert the data
        parseCSV(file_path)
        return redirect(url_for('index'))
        

        


