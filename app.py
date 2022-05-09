import os
from flask import Flask, request, render_template, redirect
from firebase_admin import credentials, firestore, initialize_app

# Initialize Flask App
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate("key.json")
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method =='POST':
        try:
            todo_ref.add({'task': request.form['task'], 'complete': False})
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        try:
            todos = []
            for doc in todo_ref.stream():
                todo = doc.to_dict()
                todo['id'] = doc.id
                todos.append(todo)
            print(todos)
            return render_template('index.html', todos=todos)
        except:
            return 'There was an issue loading your todos'


@app.route('/complete/<id>')
def complete(id):
    try:
        todo_ref.document(id).update({'completed': True})
        return redirect('/')
    except:
        return 'There was an issue updating your task'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
