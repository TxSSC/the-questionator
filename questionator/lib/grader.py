import json

#relative to the runtime environment
ANSWER_FILE = 'questionator/lib/answers.json'

class Grader():
    #read in the json file
    answers = open(ANSWER_FILE, 'r').read()
    answers = json.loads(answers)
    
    #check for a correct answer
    def gradeQuestion(self, question, answer):
        try:
            if self.answers[question] == answer:
                #question is correct
                return 1
            else:
                #question is wrong
                return 0
        except KeyError:
            #question not found
            return -1

    def iterAnswers(self):
        return self.answers.iteritems()
