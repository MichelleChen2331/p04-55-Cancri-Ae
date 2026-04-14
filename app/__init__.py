from flask import Flask, render_template
from flask import session, request, redirect

app = Flask(__name__)

@app.route('/home', methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/definitions", methods=["GET", "POST"])
def definitions():
    

if __name__ == '__main__':
    app.debug = True
    app.run()
