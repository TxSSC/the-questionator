import datetime
from questionator.lib.tools import connectDB

#Submission format:
# {
#   "id": GenerateID(),
#   "completed": Datetime,
#   "score": float,
#   "answers":
#       [
#           {
#               "q1": ["wrong", "a"]
#           },
#           {
#               "q2": ["correct", "d"]
#           }
#       ]
# }

class Submission(object):
    
    def __init__(self, submission=None):
        self.database = connectDB()
        self.submission = {}

        if submission == None:
            self.uid = None
            self.score = None
            self.completed = None
            self.answers = {}
        else:
            if type(submission['answers']) != dict:
                raise KeyError('answers not a list')
            self.uid= submission['id']
            self.score = submission['score']
            self.completed = submission['completed']
            self.answers = submission['answers']

    def save(self):
        if self.uid != None and self.score != None:
            submission = {}
            submission['id'] = self.uid
            submission['completed'] = datetime.datetime.now()
            submission['answers'] = self.answers
            submission['score'] = self.score
            if not Submission.hasDuplicate(self.uid):
                self.database.submissions.save(submission)
            else:
                raise KeyError('ID already exists')
            return self
        else:
            raise KeyError('Invalid submission')

    @staticmethod
    def getSubmissions():
        database = connectDB()
        subs = []
        for item in database.submissions.find():
            subs.append(item)
        return subs

    @staticmethod
    def hasDuplicate(uid):
        database = connectDB()
        if database.submissions.find_one({'id': uid}):
            return True
        else:
            return False 
