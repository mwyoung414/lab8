import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from models import User, Todo  
from dbcontext import DBContext

app = Flask(__name__)

DBContext.init_app(app)

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

@app.route("/userlist", methods=['GET'])
def userlist():
    users = DBContext.session.query(User).all()

    if len(users) == 0:
        return jsonify({"message": "No users found"})
    
    return jsonify([user.__dict__ for user in users])

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)