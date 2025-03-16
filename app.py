import os
from datetime import datetime as DateTime
from flask import Flask, request, jsonify
from models import User, Todo  
from dbcontext import DBContext

app = Flask(__name__)

DBContext(app)

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "GET, POST, PUT, DELETE OPTIONS"
    return response

@app.route("/", methods=['GET'])
def index():
    return "Hello World from Lab 8!\n"

@app.route("/<name>", methods=['GET'])
def hello_name(name):
    return f'Hello {name}!\n'

@app.route("/adduser", methods=['POST'])
def adduser():
    try:
        data = request.get_json()
        user = User(data['name'], data['email'], data['password'], DateTime.now())
        DBContext.addUser(user)
        DBContext.close()
        return jsonify(user.__dict__)
    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/userlist", methods=['GET'])
def userlist():
    users = DBContext.session.query(User).all()
    
    if len(users) == 0:
        return jsonify({"message": "No users found"})
    
    return jsonify([user.__dict__ for user in users])

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)