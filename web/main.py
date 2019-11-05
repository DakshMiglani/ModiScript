from flask import Flask, request, jsonify
from flask_cors import CORS
from modiscript.api import ModiScript
from modiscript.utils import ErrorHandler

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

ms = ModiScript()

@app.route("/", methods=["POST"])
def run():
    body = request.get_json(silent=True)
    code = body.get("code")

    if not code:
        return jsonify({ "error": "Executable code has not been provided." }), 400

    try:
        return jsonify({ "out": ms.execute(code, "code") }), 200
    except ErrorHandler as e:
        return jsonify({ "error": str(e) }), 402
