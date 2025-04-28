from flask import Flask, request, jsonify
from flask_cors import CORS
from db import DB

app = Flask(__name__)
CORS(app)

db = DB()

@app.route("/tasks")
def get_tasks():
    tasks = db.get_tasks()
    res = jsonify(tasks)
    return res

@app.route("/tasks", methods=["POST"])
def create_task():
    db.create_tasks(request.get_json())
    return "", 204

@app.route("/change/id", methods=["PATCH"])
def change_task_id(id):
    pass

@app.route("/change/casenum", methods=["PATCH"])
def change_task_casenum(id):
    pass

@app.route("/change/description", methods=["PATCH"])
def change_task_desc(id):
    pass

@app.route("/change/status", methods=["PATCH"])
def change_task_status():
    pass

if __name__ == '__main__':
    app.run(debug=True)
