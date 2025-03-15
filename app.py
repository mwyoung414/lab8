from flask import Flask, request, jsonify
import json

app = Flask(__name__)

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

@app.route("/todos", methods=['GET'])
def todo_list():
    service = Service()
    return jsonify(service.get_todos())

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)