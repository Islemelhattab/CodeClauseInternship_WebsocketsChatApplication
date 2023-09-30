from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store user information (sid -> username)
users = {} 
@socketio.on("message")
def sendMessage(data):
    username = data["username"]
    message = data["message"]
    send({"username": username, "message": message}, broadcast=True)


@socketio.on("connect")
def handle_connect():
    sid = request.sid
    users[sid] = ""
    emit("update_users", list(users.values()), broadcast=True)


@socketio.on("set_username")
def handle_set_username(data):
    sid = request.sid
    username = data["username"]
    users[sid] = username
    emit("update_users", list(users.values()), room=sid) 

@app.route("/")
def message():
    return render_template("message.html")


if __name__ == "__main__":
    socketio.run(app, debug=True)


