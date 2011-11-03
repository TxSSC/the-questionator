import model_helpers


class Question(object):

    def __init__(self, question=None):
        self.database = model_helpers.connectDB()
        self.question = {}
        if question == None:
            self.text = None
            self.name = None
            self.answers = []
        else:
            try:
                self.text = question['text']
                self.name = question['name']
                self.answers = question['answers']
            except KeyError:
                raise KeyError('Invalid question object.')

    def save(self):
        if self.question != None and self.name != None and self.answers != None:
            question = {}
            question['text'] = self.question
            question['name'] = self.name
            question['answers'] = self.answers
            if self.database.questions.find({'name': self.name}).count() == 0:
                self.database.save(self.question)
            else:
                raise KeyError('Duplicate name in questions')
        else:
            raise KeyError('Invalid question')

        return self

    @staticmethod
    def getQuestions():
        database = model_helpers.connectDB()
        questions = []
        for question in database.questions.find():
            questions.append(question)

        return questions
