from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'shai1995'


if __name__ == "__main__":
    app.run()
