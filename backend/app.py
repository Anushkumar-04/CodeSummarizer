from flask import Flask, request, jsonify
from flask_cors import CORS
from pycparser import c_parser, c_ast
import json

app = Flask(__name__)
CORS(app)

def ast_to_dict(node):
    if isinstance(node, c_ast.Node):
        result = {"_type": type(node).__name__}
        for attr, child in node.children():
            result[attr] = ast_to_dict(child)
        return result
    else:
        return str(node)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    code = file.read().decode("utf-8")

    try:
        parser = c_parser.CParser()
        ast = parser.parse(code)
        ast_json = ast_to_dict(ast)
        return jsonify({"ast": ast_json})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
