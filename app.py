from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

@app.route('/edit')
def home1():
    return render_template('base.html', todos=Todo.query.all())

@app.route('/')
def list1():
    return render_template('list.html', todos=Todo.query.all())

@app.route('/add', methods=['POST'])
def add():
    todo = Todo(title=request.form['title'], complete=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('home1'))

@app.route('/update/<string:id>')
def update(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = True
    db.session.commit()
    return redirect(url_for('home1'))

@app.route('/delete/<string:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home1'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)