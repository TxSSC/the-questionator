from flask import request, session, redirect, url_for
from flask import render_template, flash, Blueprint
from questionator.models.question import Question
from questionator.models.submission import Submission
from questionator.lib.tools import gradeTest, Paginator, generateID
from questionator import app

#root route - generate random id
@app.route('/')
def start():
    """Generate a random id from the systime and assign set id in the session
    won't allow you to generate a new id on refresh.
    """
    #test session has been started
    if session.has_key('id'):
        return render_template('index.html', id=session['id'], error="Unique ID has already been generated,")

    randId = generateID()
    #continue to generate a new id if records are returned
    while (Submission.hasDuplicate(randId)):
        randId = generateID()
    
    #start the session
    session['id'] = randId
    return render_template('index.html', id=randId)


#generate the test document
@app.route('/test/', defaults={'page': 1}, methods=['GET'])
@app.route('/test/page/<int:page>', methods=['POST', 'GET'])
def test(page):
    """Checks that id has been set in the session and renders the test template if so, if
    id has not been set it redirects back to start."""
    if session.has_key('id'):
        num_questions = Question.questionCount()
        if not num_questions:
            abort(404)

        #start a test session if not already started
        if not session.has_key('test'):
            temp_test = {}
            session['test'] = temp_test
        #check for answers, if any, to save
        if request.method == 'POST':
            temp_test = session['test']
            for k, v in request.form.iteritems():
                temp_test[k] = v
            session['test'] = temp_test
        #how many questions per page?
        PER_PAGE = 10
        #paginate questions
        paginate = Paginator(page, PER_PAGE, num_questions)
        return render_template('test.html', questions=Question.getPage(page, PER_PAGE), pagination=paginate, page=page)

    else:
        return redirect(url_for('start'))


#grade the test
@app.route('/test/submit/', methods=['POST'])
def submit():
    """Creates a new record, assigning it the id from the session, and grades the test using
    questionator/lib/answers.json. After grading the test, it will set the score in the session to the users score."""
    record = Submission()
    if session.has_key('id'):
        record.uid = session['id']
    else:
        return redirect(url_for('start'))

    #check to make sure they haven't submitted the test multiple times
    if (Submission.hasDuplicate(record.uid)):
        flash('You have already submitted your test')

    #save the last answers if any
    user_test = session['test']
    for k, v in request.form.iteritems():
        user_test[k] = v
    session['test'] = user_test
    
    #grade the test
    record = gradeTest(record, user_test)

    #save the record a keyerror should never happen
    try:
        record.save()
    except KeyError:
        #log on record save failure
        app.logger.error('Record %d failed to save.', record.uid)

    session['score'] = record.score

    return redirect(url_for('results'))


@app.route('/test/results/')
def results():
    """If an id and score are not found in the session, redirect to start. Otherwise render 
    the results template with id and score after popping id and score off the session"""
    if session.has_key('id') and session.has_key('score'):
        id = session['id']
        score = session['score']
    else:
        return redirect(url_for('start'))

    #destroy session
    session.pop('id')
    session.pop('score')
    session.pop('test')

    return render_template('results.html', id=id, score=score)
