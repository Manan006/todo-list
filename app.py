#Copyright 2021@Manan
#
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.


from flask import Flask, render_template, request, redirect
import flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
#importing requirments

load_dotenv()
#loading the dotenv to get variables fron .env

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#adding database to the flask app

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
#configuring database

@app.route('/', methods=['GET', 'POST'])
def home():
    session = flask.request.cookies.get('session')
    valid_session=os.getenv('session')
    if session==valid_session:
        #if the method is post, a new todo is to be added
        if request.method=='POST':
            title = request.form['title']
            desc = request.form['desc']
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
            #new todo added to the db
        allTodo = Todo.query.all() 
        return render_template('index.html', allTodo=allTodo)
        #rendering the webpage regardless
    else:
        return render_template('login.html')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    #checking if the request is a post one, if it is then update the db
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)
    #rendering the webpage regardless

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
    #deleting the todo from the db and rendering it again

@app.route('/login',methods=['POST'])
def login():
    password=flask.request.form['password']
    if password!=os.getenv('password'):
        return "Invalid Password"
    resp = flask.make_response(flask.redirect('/'))
    resp.set_cookie('session',os.getenv('session'))
    return resp

if __name__ == "__main__":
    app.run(debug=True, port=8080,host='0.0.0.0')

