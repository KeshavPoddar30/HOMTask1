from flask import Flask, request, jsonify
import uuid

usersCredentials = {}       # Stores usersCredentials: { username: password }
sessions = {}    # Stores tokens: { token: username }
tasks = {}       # Stores tasks: { username: [ { id, title } ] }


app = Flask(__name__)

def get_user_from_token():
    token = request.headers.get('Authorization')
    return sessions.get(token)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username in usersCredentials:
        return jsonify({"message": "User already exists"}), 400
    usersCredentials[username] = password
    tasks[username] = []
    return jsonify({"message": "Registered"})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if usersCredentials.get(username) != password:
        return jsonify({"message": "Invalid credentials"}), 401
    token = str(uuid.uuid4())
    sessions[token] = username
    return jsonify({"token": token})


@app.route("/tasks", methods=["POST"])
def add_task():
    user = get_user_from_token()
    if not user:
        return jsonify({"message": "Unauthorized"}), 401
    data = request.get_json()
    task = {"id": str(uuid.uuid4()), "title": data.get("title")}
    tasks[user].append(task)
    return jsonify({"message": "Task added"})


@app.route("/tasks", methods=["GET"])
def get_tasks():
    user = get_user_from_token()
    if not user:
        return jsonify({"message": "Unauthorized"}), 401
    return jsonify(tasks[user])


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    user = get_user_from_token()
    if not user:
        return jsonify({"message": "Unauthorized"}), 401
    tasks[user] = [t for t in tasks[user] if t["id"] != task_id]
    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":
    app.run(debug=True)

