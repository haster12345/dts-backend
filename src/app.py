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

@app.route("/create-task", methods=["POST"])
def create_task():
    try:
        print(request.get_json())
        db.create_tasks(request.get_json())
        return jsonify({
            'status': 204
        })
    except Exception as e:
        return jsonify({
            'status': 500,
            'error': e
        })

@app.route("/delete-task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        db.delete_task({
            'id': task_id
        }
        )
        return jsonify({
            'status': 204
        })
    except Exception as e:
        return jsonify({
            'status': 500,
            'error': e
        })

@app.route("/change/id", methods=["PATCH"])
def change_task_id(old_id, new_id):
    pass

@app.route("/change/casenum/<int:task_id>/<int:case_num>", methods=["PATCH"])
def change_task_casenum(id, new_casenum):
    return db.update_task_case_number(id, new_casenum)

@app.route("/change/description", methods=["PATCH"])
def change_task_desc(id, new_description):
    pass

@app.route("/change/status", methods=["PATCH"])
def change_task_status(id):
    pass

if __name__ == '__main__':
    app.run(debug=True)
