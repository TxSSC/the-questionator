import unittest
from datetime import datetime
from pymongo import Connection
import sys
import os

path = os.path.abspath(os.path.join(os.path.curdir, '../models'))
question = os.path.abspath(os.path.join(os.path.curdir, '../../'))
if path not in sys.path:
    sys.path.append(path)
    sys.path.append(question)

from submission import Submission

class SubmissionTest(unittest.TestCase):

    def setUp(self):
        os.environ['TESTING'] = '1'

    def tearDown(self):
        conn = Connection()
        conn.drop_database('testing')
        os.environ.pop('TESTING')
    
    def test_creation(self):
        s = {'id': 45, 'completed': datetime.now(), 'score': 40, 'answers':
                {'q1': 'Correct', 'q2': 'Wrong', 'q3': 'Wrong', 'q4': 'Correct', 'q5': 'Wrong'}
            }
        sub = Submission(s)
        assert sub.uid == s['id'] and sub.completed == s['completed'] and sub.score == s['score'] and sub.answers == s['answers']
        sub.save()

    def test_blank_name(self):
        sub = Submission()
        sub.id = 1
        try:
            sub.save()
        except KeyError, e:
            print 'Adding blank submission failed: %s' % e

    def test_duplicate(self):
        s = {'id': 30, 'completed': datetime.now(), 'score': 40, 'answers':
                {'q1': 'Correct', 'q2': 'Wrong', 'q3': 'Wrong', 'q4': 'Correct', 'q5': 'Wrong'}
            }
        sub = Submission(s)
        sub.save()
        try:
            sub.save()
        except KeyError, e:
            print 'Failed trying to save duplicate: %s' % e
        assert Submission.hasDuplicate(sub.uid)
        assert sub.uid == s['id'] and sub.completed == s['completed'] and sub.score == s['score'] and sub.answers == s['answers']

    def test_getSubmissions(self):
        #check that getSubmissions() returns the same amount of rows as mongo
        stat = len(Submission.getSubmissions())
        mon = Connection().testing.subs
        mon = mon.find().count()
        assert mon == stat


if __name__ == '__main__':
    unittest.main()
