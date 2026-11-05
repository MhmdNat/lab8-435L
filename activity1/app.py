from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    # 0.0.0.0 so the app can be reached from outside the container
    app.run(host='0.0.0.0', port=5000)
