from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tasks = []
next_id = 1

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    global next_id
    task = request.json
    if not task or 'title' not in task or 'topic' not in task:
        abort(400)

    task['id'] = next_id
    next_id += 1
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<string:title>', methods=['GET'])
def get_task_id(title):  # Use the title from the URL path
    # Search for the task
    task_id = None
    for task in tasks:  # Iterate through the list of tasks
        if task['title'] == title:  # Check if the task title matches
            task_id = task['id']  # Retrieve the task ID
            break

    # If the task is found, return its ID
    if task_id:
        return jsonify({'id': task_id}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    print(tasks)
    tasks = [task for task in tasks if task['id'] != task_id]
    return '', 204  # No Content

if __name__ == '__main__':
    app.run(debug=True)