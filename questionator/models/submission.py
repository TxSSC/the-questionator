import datetime
from questionator.lib.tools import connectDB


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
                raise KeyError('answers not a dict')
            self.uid= submission['id']
            self.answers = submission['answers']

    def hasDuplicate(self):
        if self.database.submissions.find_one({'id': self.uid}):
            return True
        else:
            return False

    def save(self):
        if self.uid != None and self.score != None:
            submission = {}
            submission['id'] = self.uid
            submission['completed'] = datetime.datetime.now()
            submission['answers'] = self.answers
            submission['score'] = self.score
            if not self.hasDuplicate():
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
