from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, Queue
import os
from twilio.rest import Client

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = "development"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand) #init migrate update downgrade

queue = Queue()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/new', methods=['POST'])
def _new():
    #_queue.enqueue(item)
    name = request.json.get('name', None)

    if name:
        info = request.get_json()
        queue.enqueue(info)
        return jsonify({"msg": f"{name} was added to the queue."}), 200
    else:
        return jsonify({"msg": "You have to provide any name."}),401

@app.route('/next', methods=['GET'])
def _next():
    return jsonify({"msg": f"{queue.dequeue()} is no longer in the queue."})
    

@app.route('/all', methods=['GET'])
def _all():
    queue.get_queue()
    return jsonify({"msg": f"A list with {queue.size()} entries has been send."})

if __name__ == '__main__':
    manager.run()
