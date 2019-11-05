import sys
sys.path.append("..")

from flask import Flask, request, jsonify
from flask_cors import CORS
from modiscript.api import ModiScript
from modiscript.utils import ErrorHandler
from io import StringIO
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

ms = ModiScript()

def captureOutput(func):
    def inner(*args, **kwargs):
        sys.stdout = StringIO()

        func(*args, **kwargs)

        return sys.stdout.getvalue()
    return inner

@captureOutput
def execute(code):
    ms.execute(code, "code")


@app.route("/", methods=["POST"])
def run():
    body = request.get_json(silent=True)
    code = body.get("code")

    if not code:
        return jsonify({ "error": "Executable code has not been provided." }), 400

    try:
        return jsonify({ "out": execute(code) }), 200
    except ErrorHandler as e:
        return jsonify({ "error": str(e) }), 402
