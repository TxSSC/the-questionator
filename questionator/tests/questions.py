import unittest
from pymongo import Connection
import sys
import os

path = os.path.abspath(os.path.join(os.path.curdir, '../models'))
question = os.path.abspath(os.path.join(os.path.curdir, '../../'))
if path not in sys.path:
    sys.path.append(path)
    sys.path.append(question)

from question import Question

class QuestionTest(unittest.TestCase):

    def setUp(self):
        os.environ['TESTING'] = '1'

    def tearDown(self):
        conn = Connection()
        conn.drop_database('testing')
        os.environ.pop('TESTING')
    
    def test_creation(self):
        q = {'name': 'q1', 'text': 'Random question one, choose a.', 'answers': 
                [{'value': 'a', 'text': 'a'}, {'value': 'b', 'text': 'b'}, 
                 {'value': 'c', 'text': 'c'},{'value': 'd', 'text': 'd'}]
            }
        question = Question(q)
        assert question.name == q['name'] and question.text == q['text'] and question.answers == q['answers']
        question.save()

    def test_blank_name(self):
        question = Question()
        question.text = 'Blank test question'
        question.answers = []
        try:
            question.save()
        except KeyError, e:
            print 'Adding blank question failed: %s' % e

    def test_duplicate(self):
        q = {'name': 'q2', 'text': 'Random question one, choose a.', 'answers': 
                [{'value': 'a', 'text': 'a'}, {'value': 'b', 'text': 'b'}, 
                 {'value': 'c', 'text': 'c'},{'value': 'd', 'text': 'd'}]
            }
        question = Question(q)
        assert question.name == q['name'] and question.text == q['text'] and question.answers == q['answers']
        question.save()
        try:
            question.save()
        except KeyError, e:
            print 'Trying to save duplicate: %s' % e

    def test_getQuestions(self):
        #check that getQuestions() returns the same amount of rows as mongo
        stat = len(Question.getQuestions())
        mon = Connection().testing.questions
        mon = mon.find().count()
        assert mon == stat


if __name__ == '__main__':
    unittest.main()
