import os
import subprocess
from typing import Tuple, Union
from flask import Flask, request, jsonify, Response

app: Flask = Flask(__name__)

# Constants
SUPPORTED_COMMANDS: list = ['ls', 'cat']
ERROR_UNSUPPORTED_COMMAND: str = "Unsupported command"
ERROR_PATH_IS_NOT_FILE: str = "Error: path is not a file"
ERROR_PATH_DOES_NOT_EXIST: str = "Error: path does not exist"
ERROR_PATH_IS_NOT_DIRECTORY: str = "Error: path is not a directory"


def is_valid_path(path: str) -> bool:
    return os.path.exists(path) and not (';' in path or '&' in path or '|' in path)


@app.route('/ls', methods=['GET'])
def list_directory() -> Tuple[Union[str, Response], int]:
    path: str = request.args.get('path', '')
    if not is_valid_path(path):
        return ERROR_PATH_DOES_NOT_EXIST, 400
    if os.path.isdir(path):
        result: subprocess.CompletedProcess[str] = subprocess.run(['ls', '-lh', path], stdout=subprocess.PIPE,
                                                                  stderr=subprocess.PIPE, text=True)
        return result.stdout if result.returncode == 0 else result.stderr, 200
    else:
        return ERROR_PATH_IS_NOT_DIRECTORY, 400


@app.route('/cat', methods=['GET'])
def cat_file() -> Tuple[str, int]:
    path: str = request.args.get('path', '')
    if not is_valid_path(path):
        return ERROR_PATH_DOES_NOT_EXIST, 400
    if os.path.isfile(path):
        with open(path, 'r') as file:
            return file.read(), 200
    else:
        return ERROR_PATH_IS_NOT_FILE, 400


@app.route('/json/<command>', methods=['GET'])
def json_command(command: str) -> Tuple[Response, int]:
    path: str = request.args.get('path', '')
    if command not in SUPPORTED_COMMANDS:
        return jsonify({"error": ERROR_UNSUPPORTED_COMMAND}), 400
    if not is_valid_path(path):
        return jsonify({"error": ERROR_PATH_DOES_NOT_EXIST}), 400

    if command == 'ls':
        if os.path.isdir(path):
            result = subprocess.run(['ls', '-lh', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return jsonify({"output": result.stdout if result.returncode == 0 else result.stderr}), 200
        else:
            return jsonify({"error": ERROR_PATH_IS_NOT_DIRECTORY}), 400

    if command == 'cat':
        if os.path.isfile(path):
            with open(path, 'r') as file:
                return jsonify({"output": file.read()}), 200
        else:
            return jsonify({"error": ERROR_PATH_IS_NOT_FILE}), 400


if __name__ == '__main__':
    port: int = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
