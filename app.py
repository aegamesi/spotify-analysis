from flask import Flask
app = Flask(__name__)
app.debug = True

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
        return 'You want path: %s' % path

@app.route('/')
def hello_world():
    return 'Hello, World!'
