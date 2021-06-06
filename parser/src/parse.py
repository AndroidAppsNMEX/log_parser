import time, os
import datetime
import mysql.connector
import glob
from multiprocessing import Pool

# Waiting for DB to br up & running
time.sleep(30)


# Log class to preload files in background, as well as keep loading files,
# while they are being populated
class Log():
    def __init__(self, filename):
        self.mydb = mysql.connector.connect(host='db',
                                            user='root',
                                            passwd=self.__read_password_secret(self),
                                            db='logs')
        self.cursor = self.mydb.cursor()
        self.filename = filename

    @staticmethod
    def __read_password_secret(self):
        # file = open('/run/secrets/db-password', 'r')
        # password = file.readlines()
        # file.close()
        return "pepe"

    #Load the entire file by using SQL. Much more quicker
    def initial_load(self):
        self.cursor.execute(
            f"""load data infile '{self.filename}' into table logs
            fields terminated by ' '
            (@col1, @col2, @col3)
            set unix_timestamp = @col1/1000,
                from_host = @col2,
                to_host = @col3,
                log_datetime = FROM_UNIXTIME(@col1/1000);""")
        self.mydb.commit()

    def parse_line(self, line):
        elements = line.split()
        unix_timestamp = int(elements[0]) / 1000
        from_host = elements[1]
        to_host = elements[2]
        p = datetime.datetime.fromtimestamp(unix_timestamp)
        data = (unix_timestamp, p, from_host, to_host)
        self.cursor.execute(
            'INSERT INTO logs (unix_timestamp, log_datetime, from_host, to_host) VALUES (%s, %s, %s, %s);',
            data)
        self.mydb.commit()


## Class to initialise MySQL DB
class DBManager:
    def __init__(self):
        self.mydb = mysql.connector.connect(host='db',
                                            user='root',
                                            passwd=self.__read_password_secret(self),
                                            db='logs')
        self.cursor = self.mydb.cursor()

    # Init Database
    def init_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS logs')
        self.cursor.execute(
            'CREATE TABLE logs (id INT AUTO_INCREMENT PRIMARY KEY, unix_timestamp BIGINT, log_datetime timestamp, from_host varchar(100), to_host varchar(100), loaddate TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
        self.mydb.commit()

    @staticmethod
    def __read_password_secret(self):
        return "pepe"


## Main method to process the files
def process_file(filename):
    logs = Log(filename)
    logs.initial_load()
    file = open(filename, "r")
    print(filename, flush=True)

    ## Go to last line
    st_results = os.stat(filename)
    st_size = st_results[6]
    file.seek(st_size)

    ## Wait for a new line
    while 1:
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
        else:
            logs.parse_line(line)


## Init database
DBManager().init_db()

## Create processes pool
pool = Pool()
## Create process per file
results = pool.map(process_file, [name for name in glob.glob("/data/logs/*.txt")])
