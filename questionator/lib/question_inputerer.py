import pymongo
import json
import os
import sys

path = os.path.abspath(os.path.join(os.path.curdir, '../../'))
if path not in sys.path:
    sys.path.append(path)

from questionator.models.question import Question
from questionator.lib.tools import connectDB


def get_questions():
    count = int(raw_input('Number of questions to enter: '))
    answers = {}
    for i in range(count):
        question = Question()
        question.name = 'q' + str(i)
        question.text = raw_input('Enter question #' + str(i) + ': ')
        question.answers = []
        
        items = 'abcde'
        for c in items:
            answer = {}
            answer['text'] = raw_input('Enter answer ' + c + ': ')
            answer['value'] = c
            question.answers.append(answer)
            cont = raw_input('Enter another question(y/n)?: ')
            if 'y' not in cont:
                break
        #get the correct answer
        cor = raw_input('What letter was the correct answer for this question?: ')
        answers[question.name] = cor
        #save the new question
        try:
            question.save()
        except KeyError:
            print 'Duplicate questions name - you must clear the database first.'
            
    
    #write the answers to answers.json.temp
    answers_file = open('./lib/answers.json.temp', 'r')
    answers_file.write(json.dumps(answers))
    answers_file.close()

    return



if __name__ == '__main__':
    get_questions()
