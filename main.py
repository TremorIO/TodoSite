from turtle import title
from flask import url_for, render_template, redirect, request, Flask
from flask_sqlalchemy import SQLAlchemy 
import os

current_dir = os.path.dirname(__file__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_dir, 'ToDo.db')

db = SQLAlchemy(app)

class ToDoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    summary = db.Column(db.Text)
    note_content = db.Column(db.Text)
    status = db.Column(db.String(12))

@app.route("/")
def index():
    notes = ToDoList.query.all()
    return render_template("index.html", notes=notes)

@app.route("/todo/<int:the_id>")
def todo(the_id):
    item = ToDoList.query.filter_by(id=the_id).one()
    return render_template("todo.html", item=item)

@app.route("/addnote")
def addnote():
    return render_template("addnote.html")

@app.route("/addpost", methods=['POST'])
def addpost():
    title = request.form['the-title']
    subtitle = request.form['the-subtitle']
    summary = request.form['the-summary']
    content = request.form['the-content']
    the_note = ToDoList(title=title, subtitle=subtitle, summary=summary, note_content=content, status="W.I.P")
    db.session.add(the_note)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)