from questionator.lib.grader import gradeTest
import time
import random
from flask import request, session, redirect, url_for
from flask import render_template, flash, Blueprint
from questionator.models.question import Question
from questionator.models.submission import Submission
from questionator import app

#root route - generate random id
@app.route('/')
def start():
    """Generate a random id from the systime and assign set id in the session
    won't allow you to generate a new id on refresh.
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
@app.route('/test/')
def test():
    """Checks that id has been set in the session and renders the test template if so, if
    id has not been set it redirects back to start."""
    try:
        if session['id']:
            return render_template('test.html', questions=Question.getQuestions())
    except KeyError:
        return redirect(url_for('start'))


#grade the test
@app.route('/test/submit/', methods=['POST'])
def submit():
    """Creates a new record, assigning it the id from the session, and grades the test using
    questionator/lib/answers.json. After grading the test, it will set the score in the session to the users score."""
    record = Submission()
    try:
        record.uid = session['id']
    except KeyError:
        return redirect(url_for('start'))

    #check to make sure they haven't submitted the test multiple times
    if (record.hasDuplicate()):
        flash('You have already submitted your test')

    #grade the test
    record = gradeTest(record, request.form)

    #save the record
    try:
        record.save()
    except KeyError:
        pass

    session['score'] = record.score

    return redirect(url_for('results'))


@app.route('/test/results/')
def results():
    """If an id and score are not found in the session, redirect to start. Otherwise render 
    the results template with id and score after popping id and score off the session"""
    try:
        id = session['id']
        score = session['score']
    except KeyError:
        return redirect(url_for('start'))

    session.pop('id')
    session.pop('score')

    return render_template('results.html', id=id, score=score)
