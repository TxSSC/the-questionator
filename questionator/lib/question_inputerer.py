import pymongo
import json
import os
import sys

path = os.getcwd()
if path not in sys.path:
    sys.path.append(path)

from questionator.models.question import Question
from questionator.lib.tools import connectDB


def get_questions():
    count = int(raw_input('Number of questions to enter: '))
    answers = {}
    for i in range(0, count):
        question = Question()
        question.name = 'q' + str(i)
        question.text = raw_input('Enter question #' + str(i+1) + ': ')
        question.answers = []
        
        items = 'abcde'
        for c in items:
            answer = {}
            answer['text'] = raw_input('Enter answer ' + c + ': ')
            answer['value'] = c
            question.answers.append(answer)
            cont = raw_input('Enter another answer(n to exit)?: ')
            if 'n' in cont:
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
    answers_file = open('answers.json.temp', 'w')
    answers_file.write(json.dumps(answers))
    answers_file.close()

    return



if __name__ == '__main__':
    get_questions()
