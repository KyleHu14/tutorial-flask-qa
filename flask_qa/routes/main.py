from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from flask_qa.extensions import db 
from flask_qa.models import Question, User 

main = Blueprint('main', __name__)

@main.route('/')
def index():
    questions = Question.query.filter(Question.answer != None).all()

    for question in questions:
        print('\n\n')
        print(question.question)

    return render_template('home.html', questions = questions)

@main.route('/ask', methods = ['GET', 'POST'])
@login_required
def ask():
    
    if request.method == 'POST':
        question_str = request.form['question']
        expert = request.form['expert']

        question = Question(question=question_str, expert_id = expert, asker_id = current_user.id)

        db.session.add(question)
        db.session.commit()

        return redirect(url_for('main.index'))

    experts = User.query.filter_by(expert=True)

    context = {
        'experts' : experts
    }
    return render_template('ask.html', **context)

@main.route('/answer/<int:question_id>', methods = ['GET', 'POST'])
@login_required
def answer(question_id): 
    if not current_user.expert:
        return redirect(url_for('main.index'))
    question = Question.query.get_or_404(question_id).first()

    if request.method == 'POST':
        question.answer = request.form['answer']
        db.session.commit()

        return redirect(url_for('main.unanswered'))


    return render_template('answer.html', question = question)

@main.route('/question/<int:question_id>')
def question(question_id):
    question = Question.query.get_or_404(question_id)

    return render_template('question.html', question = question)

@main.route('/unanswered')
@login_required
def unanswered():
    if not current_user.expert:
        return redirect(url_for('main.index'))

    noans_questions = Question.query.filter_by(expert_id = current_user.id).filter(Question.answer == None)
    
    return render_template('unanswered.html', unanswered_questions = noans_questions)

@main.route('/users')
@login_required
def users():
    if not current_user.admin:
        return redirect(url_for('main.index'))

    users = User.query.filter_by(admin=False).all()
     
    return render_template('users.html', users = users)

@main.route('/promote/<int:user_id>')
@login_required
def promote(user_id):
    if not current_user.admin:
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)
    user.expert = True
    db.session.commit()
    
    return redirect(url_for('main.users'))
