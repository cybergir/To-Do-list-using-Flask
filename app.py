from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the ToDo model
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)

# Home route to display tasks
@app.route('/')
def index():
    todo_list = ToDo.query.all()
    return render_template('index.html', todo_list=todo_list)

# Add new task
@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    new_task = ToDo(task=task, complete=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

# Update task (mark as complete)
@app.route('/update/<int:task_id>')
def update(task_id):
    task = ToDo.query.get(task_id)
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for('index'))

# Delete task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = ToDo.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()  # Create the database
    app.run(debug=True)
