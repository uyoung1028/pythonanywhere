from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import *


app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///todolists'
# # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
# app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
# db.init_app(app)
# migrate = Migrate(app,db)

#app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///movie'
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="uyoung", # 위 사진의 파란색 영역값
    password="multi1003", # MySQL 설정 초반의 비밀번호
    hostname="uyoung.mysql.pythonanywhere-services.com", # 위 사진의 빨간색 영역값
    databasename="uyoung$default", # 위 사진의 초록색 영역값
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)


@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.deadline.asc()).all()
    return render_template('index.html', todos=todos)
    
@app.route('/todos/create', methods=["GET","POST"])
def create():
    if request.method == "POST":
        todo = Todo(request.form['todo'],request.form['deadline'])
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    return render_template('create.html')
    
@app.route('/todos/<int:id>/upgrade', methods=["POST","GET"])
def upgrade(id):
    todo = Todo.query.get(id)  # 기존의 데이터 찾기
    if request.method == "POST":
        todo.todo = request.form['todo']
        todo.deadline = request.form['deadline']
        
        db.session.commit()
        
        return redirect('/')
        
    return render_template('edit.html', todo=todo)

@app.route('/todos/<int:id>/delete') 
def delete(id):
    todo = Todo.query.get(id)
    # DELETE FROM posts WHERE id=3;
    db.session.delete(todo)
    db.session.commit()
    
    return redirect('/')
    
    
@app.route('/keyboard')
def keyboard():
    keyboard = {
        "type" : "buttons",
        "buttons": ["긴급", "투두"]
    }
    return jsonify(keyboard)

@app.route('/message', methods=["POST"])
def message():
    todos = Todo.query.order_by(Todo.deadline.asc()).all()  # 객체
    user_msg = request.json['content']
    msg = '기본응답'
    url = '기본주소'
    
    li = [(i.todo, i.deadline.strftime("%Y년 %m월 %d일")) for i in todos]
        
    if user_msg == '긴급':
        msg = li[0][0] + '/' + str(li[0][1])
        
        return_dict = {
            'message': {
                'text': msg
                },
            'keyboard': {
                "type" : "buttons",
                "buttons" : ["긴급", "투두"]
            }
        }
        return jsonify(return_dict)
    
    elif user_msg == '투두':
        msg = 'Todo'
    
        return_dict = {
            'message': {
                'text': msg,
                'message_button': {
                    'label':'Todo',
                    'url': 'http://uyoung-uyoung1028.c9users.io:8080/'
                    }
                
            },
            'keyboard': {
                "type" : "buttons",
                "buttons" : ["긴급", "투두"]
            }
        }
        return jsonify(return_dict)



