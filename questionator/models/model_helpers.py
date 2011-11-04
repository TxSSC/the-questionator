from pymongo import Connection
import os

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
    #block accounts for a unit testing != None
    try:
        if os.environ['TESTING'] != None:
            database = connection['testing']
        else:
            database = connection['testing']
    except KeyError:
        database = connection[db_database]
    return database 
