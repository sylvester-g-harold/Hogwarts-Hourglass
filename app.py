from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World yo yo!"

@app.route("/1")
def pork():
	return "Human hair is underrepresented in government."

if __name__ == "__main__":
    app.run(debug=True)