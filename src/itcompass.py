from flask import Flask, render_template, session, request, url_for, redirect, abort
from json import load
from random import randint


app = Flask(__name__)
app.secret_key = b'\x03`\xc1S\x15\xcei\x17\xebI\xa8\x9a+\x8c\xa01v\x1f\xb6Q\x7f\xc5\xdb\xbb2(\x06\x9bC/\xedU'
app.config['debug'] = False

questions_file = open('questions.json', 'r')
questions = load(questions_file)
n = len(questions)
questions_file.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET': 
        return render_template('index.html')
    
    if request.method == 'POST':    
        session['x_axis'] = 0
        session['y_axis'] = 0
        return redirect(url_for('quiz', q=1))


@app.route('/quiz/<int:q>', methods=['GET', 'POST'])
def quiz(q): 
    if request.method == 'GET': 
        if q in range(1, n+1):
            data = {
                'n': n,
                'q': q,
                'question': questions[str(q)],
                'session': session,
                'debug': app.config['debug']
            }
            return render_template('quiz.html', data=data)
        else:
            return abort(404, description='Question not found')
    
    if request.method == 'POST':
        if not 'value' in request.form:
            data = {
                'n': n,
                'q': q,
                'question': questions[str(q)],
                'session': session,
                'debug': app.config['debug'],
                'error': True
            }
            return render_template('quiz.html', data=data)

        form_value = int(request.form['value'])
        # if str(q) in session or session[str(q)] != request.form['value']:
        if str(q) in session:
            session['x_axis'] -= session[str(q)] * questions[str(q)]['x_multiplier']
            session['y_axis'] -= session[str(q)] * questions[str(q)]['y_multiplier']

        session[str(q)] = form_value
        session['x_axis'] += form_value * questions[str(q)]['x_multiplier']
        session['y_axis'] += form_value * questions[str(q)]['y_multiplier']

        if q < n:
            return redirect(url_for('quiz', q=q+1))
        if q == n:
            return redirect(url_for('result'))


@app.route('/result')
def result():
    if not 'x_axis' in session:
        return redirect(url_for('index'))
    if session['x_axis'] > 24:
        session['x_axis'] = 24
    if session['y_axis'] > 24:
        session['y_axis'] = 24
    return render_template('result.html', data=session)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('wtf.html'), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0')
