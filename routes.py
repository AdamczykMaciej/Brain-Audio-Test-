from builtins import Exception

from flask import Flask, render_template, request
import psycopg2
import traceback
import logging
import redis
import json
import csv
import os
import logging
import sys

# 1st option) we can run docker with redis (there's only a fork on Windows) and specify ports
# $docker run -p 55000:6379 redis
# then check if redis running with $docker ps
# r = redis.Redis(port=55000, decode_responses=True)
# 2nd option) hosting #heroku
# it takes from environment variables (in the system)
# username = os.environ.get('USER_POSTGRES')
# password = os.environ.get('PASSWORD_POSTGRES')
#it reads from a file
#local
with open('.env', 'r') as fh:
    vars_dict = dict(
        tuple(line.strip('\n').split('='))
        for line in fh.readlines() if not line.startswith('#') or line.startswith('\n')
    )

username = vars_dict['USER_POSTGRES']
password = vars_dict['PASSWORD_POSTGRES']
#
# print(username)
# print(password)
# r = redis.Redis(host="redis-17386.c89.us-east-1-3.ec2.cloud.redislabs.com", port=17386, username=username,
#                 password=password, decode_responses=True)

app = Flask(__name__)
# app.logger.addHandler(logging.StreamHandler(sys.stdout))
# app.logger.setLevel(logging.ERROR)
# app.logger.info(username+","+password)
# two decorators, same function


try:
    # Connect to an existing database
    connection = psycopg2.connect(user=username,
                                  password=password,
                                  host="ella.db.elephantsql.com",
                                  port="5432",
                                  database=username)

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except Exception as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")




@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', the_title='Brain Test - Welcome Page')

@app.route('/instructions')
def instuctions():
    return render_template('instructions.html', the_title='Brain Test - Welcome Page')

@app.route('/audio1')
def audio1():
    return render_template('audio1.html', the_title='Brain Test')

@app.route('/audio2')
def audio2():
    return render_template('audio2.html', the_title='Brain Test')

@app.route('/audio3')
def audio3():
    return render_template('audio3.html', the_title='Brain Test')

@app.route('/audio4')
def audio4():
    return render_template('audio4.html', the_title='Brain Test')

@app.route('/audio5')
def audio5():
    return render_template('audio5.html', the_title='Brain Test')

@app.route('/audio6')
def audio6():
    return render_template('audio6.html', the_title='Brain Test')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html', the_title='Brain Test')

# ENGLISH
@app.route('/en/instructions')
def instuctions_en():
    return render_template('./EN/instructions.html', the_title='Brain Test - Welcome Page')

@app.route('/en/audio1')
def audio1_en():
    return render_template('./EN/audio1.html', the_title='Brain Test')

@app.route('/en/audio2')
def audio2_en():
    return render_template('./EN/audio2.html', the_title='Brain Test')

@app.route('/en/audio3')
def audio3_en():
    return render_template('./EN/audio3.html', the_title='Brain Test')

@app.route('/en/audio4')
def audio4_en():
    return render_template('./EN/audio4.html', the_title='Brain Test')

@app.route('/en/audio5')
def audio5_en():
    return render_template('./EN/audio5.html', the_title='Brain Test')

@app.route('/en/audio6')
def audio6_en():
    return render_template('./EN/audio6.html', the_title='Brain Test')

@app.route('/en/thanks')
def thanks_en():
    return render_template('./EN/thanks.html', the_title='Brain Test')

@app.route('/api/saveResult', methods=['POST'])
def saveResult():

    print('Incoming..')
    result = request.get_json();
    print(result)  # parse as JSON
    answers_en = {'audio1':'anger',
                  'audio2':'disgust',
                  'audio3':'fear',
                  'audio4':'happiness',
                  'audio5':'sadness',
                  'audio6':'surprise'}

    answers_pl = {'audio1':'zlosc',
                  'audio2':'obrzydzenie',
                  'audio3':'lek',
                  'audio4':'szczescie',
                  'audio5':'smutek',
                  'audio6':'zaskoczenie'}

    user_id = result['cookie'].split('=')[1]
    task = result['task']
    reactionTime = result['reactionTime']
    responseTime = result['responseTime']
    answer = result['answer']

    if result['language'] == 'en':
        with open('static/results_en.csv', 'a', newline='') as csvfile:
            is_correct = 'yes' if answer.lower() == answers_en[task].lower() else 'no'

            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            spamwriter.writerow(['userid', user_id,
                                 'Task', task,
                                 'reactionTime', reactionTime,
                                 'responseTime', responseTime,
                                 "User answer", answer,
                                 "Correct answer", answers_en[task],
                                 "Is Correct", is_correct])

        #PostgreSQL
        try:
            # Connect to an existing database
            connection = psycopg2.connect(user=username,
                                          password=password,
                                          host="ella.db.elephantsql.com",
                                          port="5432",
                                          database=username)

            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Print PostgreSQL details
            print("PostgreSQL server information")
            print(connection.get_dsn_parameters(), "\n")
            # Executing a SQL query
            values = (user_id, task, reactionTime, responseTime, answer, answers_en[task], is_correct)
            cursor.execute(
                "INSERT INTO Users(User_ID, Task, reaction_Time, Response_Time, User_Answer, Correct_Answer, Is_Correct) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                values
            )
            connection.commit()
            print("INSERTED", values)
            # print("INSERTED", values)
        except Exception as error:
            print("Error while connecting to PostgreSQL", error)

        finally:
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    else:
        with open('static/results.csv', 'a', newline='') as csvfile:
            is_correct = 'yes' if answer.lower() == answers_pl[task].lower() else 'no'

            spamwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            spamwriter.writerow(['userid', user_id,
                                 'Task', task,
                                 'reactionTime', reactionTime,
                                 'responseTime', responseTime,
                                 "User answer", answer,
                                 "Correct answer", answers_pl[task],
                                 "Is Correct", is_correct])

        #PostgreSQL
        try:
            # Connect to an existing database
            connection = psycopg2.connect(user=username,
                                          password=password,
                                          host="ella.db.elephantsql.com",
                                          port="5432",
                                          database=username)

            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Print PostgreSQL details
            print("PostgreSQL server information")
            print(connection.get_dsn_parameters(), "\n")
            # Executing a SQL query
            values = (user_id, task, reactionTime, responseTime, answer, answers_pl[task], is_correct)
            cursor.execute(
                "INSERT INTO Users(User_ID, Task, reaction_Time, Response_Time, User_Answer, Correct_Answer, Is_Correct) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                values
                    )
            connection.commit()
            print("INSERTED", values)
        except Exception as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


    # return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return 'OK', 200

if __name__ == '__main__':
    # DEBUGGING
    # r.flushdb()
    # r.mset({"Maciej":"66%"})
    # r.hmset("leaderboard",{"Bartek":"70%"})
    # r.hmset("leaderboard",{"Maciek":"80%"})
    # print(r.get("Maciej"))
    # pprint(r.keys())
    # for result in r.hscan_iter("leaderboard", match='*'):
    #     print(result)
    app.run(debug=True)
