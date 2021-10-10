from flask import Flask, request, jsonify
from  datetime import datetime
import json
import logging
import psycopg2
import os

# Flag to check if the database table birthday exists
db_check=False

# create logger with 'application'
logger = logging.getLogger('birthday')
logger.setLevel(logging.INFO)

# create file handler which logs
fh = logging.FileHandler('birthday.log')
fh.setLevel(logging.INFO)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

app = Flask(__name__)
date_format = "%Y-%m-%d"



def db_connection():
    db_username = os.environ.get('DB_USER', 'postgres')
    db_password = os.environ.get('DB_PASSWORD', 'postgres')
    db_server = os.environ.get('DB_HOST', "127.0.0.1")
    db_port = os.environ.get('DB_PORT', 5432)
    db_name = os.environ.get('DB_NAME', 'postgres')
    try:
        connection = psycopg2.connect(user=db_username,
                                  password=db_password,
                                  host=db_server,
                                  port=db_port,
                                  database=db_name)
        return connection

    except (Exception, psycopg2.Error) as error:
        logger.info("Failed to create DB connection", error) 

def create_database():
    # creating database connection.
    connection=db_connection()
    cursor = connection.cursor()
    global db_check
    # Creating birthday table
    sql_create_query = '''create table if not exists birthday
    ( 
        username varchar(20), 
        dob date
    )''';
    if not db_check:
        cursor.execute(sql_create_query)
        connection.commit()
        logger.info(' Table has been created successfully!!')
        db_check=True
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        logger.info("PostgreSQL connection is closed")

def getUserIndex(username):
    # creating database connection.
    connection=db_connection()
    cursor = connection.cursor()
    logger.info("Fetching record for {}".format(username))

    # Fetch the user details from the database
    sql_select_query = """select * from birthday where username = %s"""
    cursor.execute(sql_select_query, (username,))
    record = cursor.fetchone()
    
    #print(record)
    logger.info(' User: {}'.format(record))
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        logger.info("PostgreSQL connection is closed")
    return  record


def insertUser(username,dob):
    connection=db_connection()
    cursor = connection.cursor()

    logger.info("Inserting record for {}".format(username))
    # Insert single record now
    postgres_insert_query = """ INSERT INTO birthday (USERNAME, DOB) VALUES (%s,%s)"""
    record_to_insert = (username, dob)
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    logger.info('{} Record Inserted successfully'.format(count))

    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        logger.info("PostgreSQL connection is closed")

def updateUser(username,dob):
    connection=db_connection()
    cursor = connection.cursor()

    # Update single record now
    logger.info("Updating record for {}".format(username))

    sql_update_query = """Update birthday set DOB = %s where USERNAME = %s"""
    cursor.execute(sql_update_query, (dob, username))

    connection.commit()
    count = cursor.rowcount
    logger.info('{} Record Updated successfully'.format(count))

    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        logger.info("PostgreSQL connection is closed")
    
def deleteUsername(username):
    connection=db_connection()
    cursor = connection.cursor()

    # Update single record now
    logger.info("Deleting record for {}".format(username))

    sql_delete_query = """Delete from birthday where USERNAME = %s"""
    cursor.execute(sql_delete_query, ( username,))

    connection.commit()
    count = cursor.rowcount
    logger.info('{} Record Deleted successfully'.format(count))

    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        logger.info("PostgreSQL connection is closed")
    
@app.route("/hello/<username>", methods=["PUT"])
def InsertupdateUser(username):
    my_dict = {}
    create_database()
    user=getUserIndex(username)
    request_data = request.get_json()

    if user==None:
        # Inserting new user if the user doesn't exist
        my_dict['userName']=username
        my_dict['dateOfBirth']=request_data['dateOfBirth']
        insertUser(username,request_data['dateOfBirth'])
        logger.info('New User details: {}'.format(my_dict))
    else:
        # Updating user if the user exist
        my_dict['userName']=username
        my_dict['dateOfBirth']=request_data['dateOfBirth']
        updateUser(username,request_data['dateOfBirth'])
        logger.info('Updated User details: {}'.format(my_dict))

    return ('', 204)

@app.route('/hello/<username>', methods=['GET'])
def getHello(username):
    temp_dict={}
    create_database()

    user=getUserIndex(username)
    if user==None:
            temp_dict['message']="{}! does not exists !".format(username)
    else:
            today = datetime.today().strftime(date_format)
            today = datetime.strptime(today, date_format)
            birth = user[1]
            user =user[0]

            logger.info("Today: {}".format(today) )
            if(
                today.month == birth.month
                and today.day >= birth.day
                or today.month > birth.month
                ):
                nextBirthdayYear = today.year + 1
            else:
                nextBirthdayYear = today.year

            next_bday="{}-{}-{}".format(nextBirthdayYear,birth.month,birth.day)
            nextBirthday = datetime.strptime(next_bday, date_format)
            #print("Next birth:", nextBirthday)
            logger.info('Next birth: {}'.format(nextBirthday))
            diff = nextBirthday - today
            #print("days left for next birthday:", diff.days)
            logger.info('days left for next birthday: {}'.format(diff.days))
            logger.info('Today: {}'.format(today))

            #print("Today:", today)
            if diff.days==365 or diff.days==366:
                temp_dict['message']="Hello, {}! Happy birthday!".format(user)
            else:
                temp_dict['message']="Hello, {}! Your birthday is in {} day(s)".format(user,diff.days)
    logger.info(temp_dict)
    return  jsonify(temp_dict), 200

@app.route('/hello/<username>', methods=['DELETE'])
def deleteUser(username):
    temp_dict={}
    create_database()
    user=getUserIndex(username)
    if user==None:
        temp_dict['message']="{}! does not exists !".format(username)
    else:
        deleteUsername(username)
        temp_dict['message']="User {}! with dob {} has been deleted successfully!".format(user[0],user[1])
    logger.info(temp_dict)
    return  jsonify(temp_dict), 200


if __name__ == '__main__':
    PORT="5000"
    if PORT is not None:
        app.run(host= '0.0.0.0',debug=True, port=PORT)