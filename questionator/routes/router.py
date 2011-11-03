from questionator.lib.grader import Grader
import time
import random
from flask import request, session, redirect, url_for
from flask import render_template, flash, Blueprint
from questionator.models.question import Question
from questionator.models.submission import Submission

blueprint = Blueprint('routes', __name__, template_folder='questionator/templates/', static_folder='questionator/templates/')

#root route - generate random id
@blueprint.route('/')
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
    submission = Submission()
    submission.uid = randId
    #continue to generate a new id if records are returned
    while (submission.hasDuplicate()):
        randId = rand.randint(0, 10000)
        submission.uid = randId
    
    #start the session
    session['id'] = randId
    return render_template('index.html', id=randId)


#generate the test document
@blueprint.route('/test/')
def test():
    try:
        if session['id']:
            return render_template('test.html', questions=Question.getQuestions())
    except KeyError:
        return redirect(url_for('start'))


#grade the test
@blueprint.route('/test/submit/', methods=['POST'])
def submit():
    record = Submission()
    try:
        record.uid = session['id']
    except KeyError:
        return redirect(url_for('start'))

    #check to make sure they haven't submitted the test multiple times
    if (record.hasDuplicate()):
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

    record.score = score
    record.save()
    session['score'] = score

    return redirect(url_for('results'))


@blueprint.route('/test/results/')
def results():
    try:
        id = session['id']
        score = session['score']
    except KeyError:
        return redirect(url_for('start'))

    session.pop('id')
    session.pop('score')

    return render_template('results.html', id=id, score=score)
