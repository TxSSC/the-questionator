import unittest
from pymongo import Connection
import sys
import os
import json

lib = os.path.abspath(os.path.join(os.path.curdir, '../lib'))
models =  os.path.abspath(os.path.join(os.path.curdir, '../models'))
question = os.path.abspath(os.path.join(os.path.curdir, '../../'))

if lib not in sys.path or models not in sys.path or question not in sys.path:
    sys.path.append(lib)
    sys.path.append(models)
    sys.path.append(question)


from tools import gradeTest
from submission import Submission

class SubmissionTest(unittest.TestCase):

    def setUp(self):
        os.environ['TESTING'] = '1'

    def tearDown(self):
        conn = Connection()
        conn.drop_database('testing')
        os.environ.pop('TESTING')

    
    def test_correct(self):
        answers = json.loads(open('./answers.json', 'r').read())
        sub = Submission()
        sub.uid = 64
        sub = gradeTest(sub, answers)
        assert sub.score == float(100)

    def test_fail(self):
        answers = {"q1": "c", "q3": "b", "q2": "a", "q5": "d", "q4": "b", "q7": "w", "q6": "w", "q9": "w", "q8": "w", "q10": "w"}
        sub = Submission()
        sub.uid = 324
        sub = gradeTest(sub, answers)
        assert sub.score == float(50) 

if __name__ == '__main__':
    unittest.main()
