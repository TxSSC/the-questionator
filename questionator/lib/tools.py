import os
import json
import time
import binascii
from pymongo import Connection
from flask import request, url_for
from math import ceil


def generateID():
    randBytes = os.urandom(4)
    return binascii.hexlify(randBytes)

def gradeTest(submission,form):
    """Submission is a Submission() model, form is the default form dict of flask
    this function will return the submission object back after it has been graded."""
    #relative to the runtime environment - debug for testing
    try:
        if os.environ['TESTING'] != None:
            ANSWER_FILE = './answers.json'
        else:
            ANSWER_FILE = 'questionator/lib/answers.json'
    except KeyError:
        ANSWER_FILE = 'questionator/lib/answers.json'     #read in the json file

    answers = open(ANSWER_FILE, 'r').read()
    try:
        answers = json.loads(answers)
    except ValueError:
        #no answers found
        submission.score = 0
        return submission
    
    total = float(0)
    score = float(0)
    for name, value in answers.iteritems():
        submission.answers[name] = []
        try:
            if value == form[name]:
                submission.answers[name].append('Correct')
                score += 1
            else:
                submission.answers[name].append('Wrong')
            submission.answers[name].append(form[name])
        except KeyError:
            pass
        total += 1
    try:
        score = round(((score/total) * 100), 2)
    except ZeroDivisionError:
        score = 0
    
    submission.score = score
    return submission


def connectDB():
    try:
        db_host = os.environ['MONGODB_HOST']
        db_port = int(os.environ['MONGODB_PORT'])
        db_database = os.environ['MONGODB_DATABASE']
    except KeyError:
        db_host = 'localhost'
        db_port = 27017
        db_database = 'questionator'
    connection = Connection(db_host, db_port)
    
    #debug for unit testing != None
    try:
        if os.environ['TESTING'] != None:
            database = connection['testing']
        else:
            database = connection[db_database]
    except KeyError:
        database = connection[db_database]
    return database

#helper for pagination
def url_for_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


class Paginator(object):
    def __init__(self, page, per_page, total):
        self.page = page
        self.per_page = per_page
        self.total = total
    
    @property
    def pages(self):
        return int(ceil(self.total / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages
