from datetime import timezone
import json
import time, os
import datetime
import mysql.connector
import threading


#Waiting for DB to br up & running
time.sleep(60)


#Log class to preload files in background, as well as keep loading files,
#while they are being populated
class Log:
    def __init__(self):
        self.mydb =  mysql.connector.connect(host='db',
                               user='root',
                               passwd=self.__read_password_secret(self),
                               db='logs')
        self.cursor = self.mydb.cursor()

    @staticmethod
    def __read_password_secret(self):
        # file = open('/run/secrets/db-password', 'r')
        # password = file.readlines()
        # file.close()
        return "pepe"

    #Execute the necessary queries every hour
    def execute_query(self, from_datetime, to_datetime, host):
        file = open('/data/output/last_hour.txt', 'a')
        from_dt = from_datetime
        to_dt = to_datetime
        query_cursor = self.mydb.cursor()
        file.write(f"Time {to_datetime}" + '\n')
        query_cursor.execute(
            'SELECT distinct from_host FROM logs WHERE log_datetime between %s AND %s AND to_host = %s',
            (from_dt, to_dt, host))
        print(query_cursor.statement, flush=True)
        rows = query_cursor.fetchall()
        if len(rows) > 0:
            file.write(f"From Host to {host}" + '\n')
            for row in rows:
                file.write(row[0] + '\n')
        self.mydb.commit()
        query_cursor.execute(
            'SELECT distinct to_host FROM logs WHERE log_datetime between %s AND %s AND from_host = %s',
            (from_dt, to_dt, host))
        rows = query_cursor.fetchall()
        if len(rows) > 0:
            file.write(f"To Host from {host}" + '\n')
            for row in rows:
                file.write(row[0] + '\n')
        self.mydb.commit()
        query_cursor.execute(
            """SELECT from_host, count(1) num_connections 
               FROM logs 
               WHERE log_datetime between %s AND %s
               GROUP BY from_host
               ORDER BY num_connections DESC
               LIMIT 1
               """,
            (from_dt, to_dt))
        rows = query_cursor.fetchall()
        if len(rows) > 0:
            file.write(f"From Host with more connections" + '\n')
            for row in rows:
                file.write(row[0] + '\n')
        self.mydb.commit()
        query_cursor.close()
        file.write(f"-------------------------" + '\n')
        file.close()


## Read config file to change parameters
def read_config_file():
    config_file_name = '/config/schedule.json'
    config_file = open(config_file_name, 'r', encoding='utf-8')
    config = json.load(config_file)
    return config


## Main method to write results once every hour
def schedule_ouput(logs):
    config = read_config_file()
    previous_time = datetime.datetime.now(timezone.utc)
    current_time = datetime.datetime.now(timezone.utc)

    while 1:
        if previous_time is not None and (current_time - previous_time).total_seconds() >= 3600:
            logs.execute_query(previous_time, current_time, config["host"])
            previous_time = current_time
        else:
            time.sleep(4)
        current_time = datetime.datetime.now(timezone.utc)
        config = read_config_file()


logs = Log()
schedule_ouput(logs)
