from flask import Flask, request, jsonify
from  datetime import datetime
import json
import logging

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

users=[
   { "userName": "ashish","dateOfBirth": "2021-10-4" },
   { "userName": "ashish0","dateOfBirth": "2021-10-3" },
   { "userName": "ashish1","dateOfBirth": "2021-10-10" }
    ]
def getUserIndex(username):
    logger.info(' Users: {}'.format(users))
    index=-1
    length=len(users)
    for i in range(length):
        if users[i]['userName']==username:
            print(users[i])
            index=i
    return  index
    
@app.route("/hello/<username>", methods=["PUT"])
def InsertupdateUser(username):
    #print(users)
    my_dict = {}
    index=getUserIndex(username)
    request_data = request.get_json()

    if index>-1:
        users[index]['dateOfBirth']=request_data['dateOfBirth']
    else:
        my_dict['userName']=username
        my_dict['dateOfBirth']=request_data['dateOfBirth']
        users.append(my_dict)
        print (my_dict)
        logger.info('Dictionary: {}'.format(my_dict))

    return ('', 204)

@app.route('/hello/<username>', methods=['GET'])
def getHello(username):
    print(users)
    temp_dict={}
    i=getUserIndex(username)
    if i==-1:
            temp_dict['message']="{}! does not exists !".format(username)
    else:
            today = datetime.today().strftime(date_format)
            today = datetime.strptime(today, date_format)
            birth = datetime.strptime(users[i]["dateOfBirth"], date_format)
            user=users[i]["userName"]

            print("Today:", today)
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
            print("Next birth:", nextBirthday)
            logger.info('Next birth: {}'.format(nextBirthday))
            diff = nextBirthday - today
            print("days left for next birthday:", diff.days)
            logger.info('days left for next birthday: {}'.format(diff.days))
            logger.info('Today: {}'.format(today))

            print("Today:", today)
            if diff.days==365 or diff.days==366:
                temp_dict['message']="Hello, {}! Happy birthday!".format(user)
            else:
                temp_dict['message']="Hello, {}! Your birthday is in {} day(s)".format(user,diff.days)
    print(temp_dict)
    return  jsonify(temp_dict), 200


if __name__ == '__main__':
    PORT="5000"
    if PORT is not None:
        app.run(host= '0.0.0.0',debug=True, port=PORT)