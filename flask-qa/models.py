from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    expert = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)

    questions_asked = db.relationship(
        'Question', 
        foreign_keys = 'Question.asker_id', 
        backref = 'asker', 
        lazy = True
    )

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    asker_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expert_id  = db.Column(db.Integer, db.ForeignKey('user.id'))