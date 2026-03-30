from flask import Flask, render_template
from flask import session, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return "Home page!"

if __name__ == '__main__':
    app.debug = True
    app.run()
