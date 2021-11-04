import mysql.connector
import logging

def connector_initialization():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user='visual',
        password="12QW#$er",
        database = "visual_data",
        port = 3306
    )
    return mydb

def line_prcessing(line, time):
    values = [v.strip() for v in line.split(",")]
    sql = "INSERT INTO daily (time, PM2dot5, PM10, SO2, NO2, CO, O3, U, V, TEMP, RH, PSFC, lat, lon) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    tup1 = (str(time),)
    val = tup1 + tuple(values[:-1])
    return sql, val


def digits(name):
    return ''.join([n for n in name if n.isdigit()])


def insert_objects():
    current_path = '/root/visualization/data/daily/201301/'
    from os import listdir
    from os.path import isfile, join
    current_files = [f for f in listdir(current_path) if isfile(join(current_path, f))]
    mycursor = mydb.cursor()
    for file in current_files:
        with open(current_path + file) as f:
            lines = f.readlines()
            time = digits(file)
            logging.info(f"Processing {current_path}{file} ...")
            for i in range(1, len(lines)):
                sql, val = line_prcessing(lines[i], time)
                mycursor.execute(sql, val)
                if (i % 1000 == 0):
                    print(f"Handling {i}/{len(lines)} of {file}")
    mydb.commit()

if __name__ == "__main__":
    mydb = connector_initialization()
    logging.basicConfig(level=logging.INFO)
    logging.info("starting..")
    insert_objects()
