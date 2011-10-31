import datetime
from grader.grader import Grader
import time
import random
import json
from flaskext.mongokit import MongoKit, Document
from flask import Flask, request, session, redirect, url_for
from flask import render_template, flash


app = Flask(__name__)
app.config.from_pyfile('settings.py')


#mongo model
class Test(Document):
    __collection__ = 'scores'
    structure = {
            'id': long,
            'answers':
                {
                    'q1': unicode,
                    'q2': unicode,
                    'q3': unicode,
                    'q4': unicode,
                    'q5': unicode,
                    'q6': unicode,
                    'q7': unicode,
                    'q8': unicode,
                    'q9': unicode,
                    'q10': unicode
                },
            'score': float,
            'completed': datetime.datetime
    }
    required_fields = ['id', 'score', 'completed']
    use_dot_notation = True


db = MongoKit(app)
db.register([Test])


#root route - generate random id
@app.route('/')
def start():
    """Generate a random id from the systime
     - Needs to be better, no too good
    """
    #test session has been started
    try:
       if session['id']:
           return render_template('index.html', id=session['id'], error="Unique ID has already been generated,")
    except KeyError:
        pass

    epoch = int(time.time())
    rand = random.Random(int(time.time()))
    randId = rand.randint(0, 10000)
    
    #continue to generate a new id if records are returned
    while (db.Test.find({'id': randId}).count()):
        randId = rand.randint(0, 10000)
    
    #start the session
    session['id'] = randId
    return render_template('index.html', id=randId)


#generate the test document
@app.route('/test/')
def test():
    try:
        if session['id']:
            return render_template('test.html')
    except KeyError:
        return redirect(url_for('start'))

#grade the test
@app.route('/test/submit/', methods=['POST'])
def submit():
    record = db.Test()
    try:
        record['id'] = long(session['id'])
    except KeyError:
        return redirect(url_for('start'))

    #check to make sure they haven't submitted the test multiple times
    if (db.Test.find({'id': record['id']}).count()):
        flash('You have already submitted your test')

    #grade the test
    gradeIt = Grader()
    total = 0
    score = 0
    #loop through all keys in the form dict
    for name, value in gradeIt.iterAnswers():
        try:
            if value == request.form[name]:
                record.answers[name] = u'Correct'
                score += 1
            else:
                record.answers[name] = u'Wrong'
        except KeyError:
            pass
        total += 1
        
    try:
        score = float((score/total) * 100)
    except ZeroDivisionError:
        score = 0

    record['score'] = score
    record['completed'] = datetime.datetime.now()
    record.save()
    session['score'] = score

    return redirect(url_for('results'))


@app.route('/test/results/')
def results():
    try:
        id = session['id']
        score = session['score']
    except KeyError:
        return redirect(url_for('start'))

    session.pop('id')
    session.pop('score')

    return render_template('results.html', id=id, score=score)


#start the response loop
if __name__ == '__main__':
    app.run()
