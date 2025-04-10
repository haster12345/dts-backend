from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

tasks = [
    {
        "id":"1",
        "desc": "KINGS PS"
     }
]

@app.route("/tasks")
def get_tasks():
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def create_task():
    tasks.append(request.get_json())
    return "", 204


if __name__ == '__main__':
    app.run(debug=True)
