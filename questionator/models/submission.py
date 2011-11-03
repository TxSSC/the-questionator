import model_helpers

class Submission(object):
    
    def __init__(self, submission=None):
        self.database = model_helpers.connectDB()
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

    def hasDuplicate(self):
        if self.database.submissions.find({'id': self.uid}).count():
            return True
        else:
            return False

    def save(self):
        if self.submission['id'] != None and self.submission['score'] != None \
                and self.submission['completed'] != None:
            submission = {}
            submission['id'] = self.uid
            submission['completed'] = datetime.datetime.now()
            submission['answers'] = self.answers
            submission['score'] = self.score
            self.database.save(submission)
            return self
        else:
            raise KeyError('Invalid submission')

    @staticmethod
    def getSubmissions():
        database = model_helpers.connectDB()
        subs = []
        for item in database.submissions.find():
            subs.append(item)
        return subs
