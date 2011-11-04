import json

#relative to the runtime environment
ANSWER_FILE = 'questionator/lib/answers.json'

def gradeTest(submission,form):
    """Submission is a Submission() model, form is the default form dict of flask
    this function will return the submission object back after it has been graded."""
    #read in the json file
    answers = open(ANSWER_FILE, 'r').read()
    answers = json.loads(answers)
    
    total = 0
    score = 0
    for name, value in answers.iteritems():
        try:
            if value == form[name]:
                submission.answers[name] = 'Correct'
                score += 1
            else:
                submission.answers[name] = 'Wrong'
        except KeyError:
            pass
        total += 1
    try:
        score = float((score/total) * 100)
    except ZeroDivisionError:
        score = 0
    submission.score = score

    return submission
