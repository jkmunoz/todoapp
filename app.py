from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Julianna@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
    
class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

def __repr__(self):
    return f'<TodoList {self.id} {self.description}>'
    
class Todo(db.Model):
    __tablename__ = 'Todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=True, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=True)

def __repr__(self):
    return f'<Todo {self.id} {self.description}, list {self.list_id}>'

#with app.app_context():
 #   db.drop_all()
 #   db.create_all()

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True })

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description, completed=False)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['completed'] = todo.completed
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (400)
    else:
        return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

#@app.route('/lists/<list_id>')
#def get_list_todos(list_id):
#        return render_template('index.html', 
#        todos=Todo.query.filter_by(list_id=list_id).order_by('id')
#        .all())

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    lists = []
    todos = Todo.query.all()
    active_list = list_id
    return render_template(
        'index.html',
        todos=todos,
        lists=lists,
        active_list=active_list
    )

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000)
