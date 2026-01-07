from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app2.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    

    def __repr__(self):
        return f'<Todo {self.id} - {self.title}>'

# Routes
@app.route('/' ,methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        print(request.form["title"])
        title=request.form["title"]
        
        todo= Todo(title=title)
        db.session.add(todo)
        db.session.commit()
            
    todos = Todo.query.all()
    return render_template('index.html' , todos=todos)
@app.route('/delete <int:id>')
def delete(id):
    todo=Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
    

@app.route('/update <int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method=='POST':
        title=request.form["title"]
        todo=Todo.query.get(id)
        todo.title=title
        db.session.commit()
        return redirect('/')
    todo = Todo.query.get(id)   
    return render_template('update.html', todo=todo)

if __name__ == "__main__":
    app.run()
