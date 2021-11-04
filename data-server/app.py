import sys
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from uuid import uuid4
import requests
from waitress import serve
import requests
import logging
import mysql.connector

logger = logging.getLogger("waitress")
logger.setLevel(logging.INFO)

password = "vPybQ52DHBfWByPUQVLNuVM7LZyfZ88kNw7ucYHKbNxqXbU"

def handle_requery(s, e, t):
    start = int(s)
    end = int(e)
    time_slots = [str(start)]
    while(start != end):
        start += 100
        time_slots.append(str(start))

    print(time_slots)
    result = {}
    result['status'] = "Successful"
    result['data'] = {}
    result['data']["attribute"] = ["time", "PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "U", "V", "TEMP", "RH", "PSFC", "lat", "lon"]
    for ts in time_slots:
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM daily WHERE time = {ts}")
        myresult = mycursor.fetchall()
        print(myresult[0], type(myresult[0]))
        result['data'][ts] = []
        for item in myresult:
           result['data'][ts].append(item) 
    return jsonify(result)

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    logger.info("accessing...")
    return "<h1>TESTING"

@app.route("/query/", methods=["POST"])
def query():
    result = {}
    req = request.json
    start_time = req["start_time"]
    end_time = req["end_time"]
    req_type = req["type"]

    if req['password'] == password:
        if req_type not in ["daily", "hourly"]:
            result['status'] = "Invalid Type"
            result['data'] = ""
            return jsonify(result)
        else:
            return handle_requery(start_time, end_time, req_type)
    else:
        result['status'] = "Invalid password"
        result['data'] = ""
        return jsonify(result)
    

if __name__ == '__main__' :
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user='visual',
        password="12QW#$er",
        database = "visual_data",
        port = 3306
    )
    serve(app, host='0.0.0.0', port=5678)
