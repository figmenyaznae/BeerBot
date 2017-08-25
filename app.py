from flask import Flask
app = Flask(__name__)

@app.route("/start")
@app.route("/")
def hello():
    return "Hello, I'm still in alpha-test mode, please, don't speak to me if you are not my developer."

@app.route("/help")
def help():
	return "TBA"