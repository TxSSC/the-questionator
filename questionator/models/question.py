from questionator.lib.tools import connectDB


class Question(object):

    def __init__(self, question=None):
        self.database = connectDB()
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
        if self.text != None and self.name != None and self.answers != None:
            question = {}
            question['text'] = self.text
            question['name'] = self.name
            question['answers'] = self.answers
            if self.database.questions.find_one({'name': self.name}) == None:
                self.database.questions.save(question)
            else:
                raise KeyError('Duplicate name in questions')
        else:
            raise KeyError('Invalid question')

        return self

    @staticmethod
    def getQuestions():
        #use a generator for the iterable of questions
        database = connectDB()
        questions = []
        for question in database.questions.find():
            questions.append(question)

        return questions

    @staticmethod
    def questionCount():
        database = connectDB()
        return database.questions.count()

    @staticmethod
    def getPage(page, per_page):
        database = connectDB()
        cursor = database.questions.find().sort('name').skip((page - 1) * per_page).limit(per_page)
        for question in cursor:
            yield question
