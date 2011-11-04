import json
import os


def gradeTest(submission,form):
    """Submission is a Submission() model, form is the default form dict of flask
    this function will return the submission object back after it has been graded."""
    #relative to the runtime environment - debug for testing
    try:
        if os.environ['TESTING'] != None:
            ANSWER_FILE = '../lib/answers.json'
        else:
            ANSWER_FILE = 'questionator/lib/answers.json'
    except KeyError:
        ANSWER_FILE = 'questionator/lib/answers.json'     #read in the json file

    answers = open(ANSWER_FILE, 'r').read()
    answers = json.loads(answers)
    
    total = float(0)
    score = float(0)
    for name, value in answers.iteritems():
        try:
            if value == form[name]:
                submission.answers[name] = 'Correct'
                score += 1
            else:
                submission.answers[name] = 'Wrong'
        except KeyError:
            pass
        total += 1
    try:
        score = float((score/total) * 100)
    except ZeroDivisionError:
        score = 0
    
    submission.score = score
    return submission



def connectDB():
    from pymongo import Connection

    try:
        db_host = os.environ['MONGODB_HOST']
        db_port = int(os.environ['MONGODB_PORT'])
        db_database = os.environ['MONGODB_DATABASE']
    except KeyError:
        db_host = 'localhost'
        db_port = 27017
        db_database = 'questionator'
    connection = Connection(db_host, db_port)
    
    #debug for a unit testing != None
    try:
        if os.environ['TESTING'] != None:
            database = connection['testing']
        else:
            database = connection['testing']
    except KeyError:
        database = connection[db_database]
    return database 
