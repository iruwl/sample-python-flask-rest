#!flask/bin/python
#http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
from flask import Flask, jsonify, abort, make_response
#from flask.ext.httpauth import HTTPBasicAuth
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

#ignore slash after
app.url_map.strict_slashes = False

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@auth.get_password
def get_password(username):
    if username == 'irul':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/tasks', methods=['GET']) #, strict_slashes=False)
@auth.login_required
def get_tasks():
    return jsonify({'tasks': tasks})

#@app.route('/tasks', methods=['GET']) #, strict_slashes=False
@app.route('/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id=None):
    #if task_id == None:
    #    return jsonify({'tasks': tasks})

    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

if __name__ == '__main__':
    app.run(debug=True)
