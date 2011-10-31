import unittest
import engine
from mongokit import Connection
from flask import Flask


class UnitTests(unittest.TestCase):
    def setUp(self):
        engine.app.config['MONGODB_DATABASE'] = 'testing'
        engine.app.config['TESTING'] = True
        self.app = engine.app.test_client()

    def tearDown(self):
        conn = Connection()
        conn.drop_database('testing')

    def test_root(self):
        res = self.app.get('/')
        with self.app.session_transaction() as session:
            assert str(session['id']) in res.data

    def test_redirects(self):
        res = self.app.get('/test/', follow_redirects=True)
        assert 'Your random ID is:' in res.data
        res = self.app.get('/test/results', follow_redirects=True)
        assert 'Your random ID is:' in res.data

    def test_submission(self):
        res = self.app.get('/')
        with self.app.session_transaction() as session:
            id = session['id']
        data = {'q1': 'b', 'q2': 'a'}
        res = self.app.post('/test/submit/', data=data, follow_redirects=True)
        assert 'You made below a 70%' in res.data
        with self.app.session_transaction() as session:
            session['id'] = id
        res = self.app.post('/test/submit/', data=data, follow_redirects=True)
        assert 'You have already submitted your test' in res.data
        answers = {'q1': 'c', 'q3': 'b', 'q2': 'a', 'q5': 'd', 'q4': 'b', 
                   'q7': 'a', 'q6': 'c', 'q9': 'd', 'q8': 'a', 'q10': 'd'
        }
        res = self.app.get('/')
        res = self.app.post('/test/submit/', data=answers, follow_redirects=True)
        assert '100.0% correct' in res.data


if __name__ == '__main__':
    unittest.main()
