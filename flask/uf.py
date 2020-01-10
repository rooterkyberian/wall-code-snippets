from flask import Flask, request

app = Flask(__name__)


@app.route("/")
@app.route("/<name>")
def hello(name: str = "") -> str:
    name = name or request.remote_addr
    return f"Hello {name}!"


if __name__ == "__main__":
    app.run(debug=False)
