from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(256), nullable=False)
    deadline = db.Column(db.DateTime)

    def __init__(self,todo,deadline):
        self.todo = todo
        self.deadline = deadline
