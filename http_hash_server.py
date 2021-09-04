from flask import Flask, request, send_file
import hashlib
import os
import re
from dotenv import load_dotenv

load_dotenv()
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

app = Flask(__name__)


def get_result_dir(upload_folder, files_hash):
    return os.path.join(upload_folder + files_hash[0:2])


def get_result_path(upload_folder, files_hash):
    return os.path.join(get_result_dir(upload_folder, files_hash), files_hash)


def create_folder(upload_folder, files_hash):
    result_dir = get_result_dir(upload_folder, files_hash)
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    return result_dir


def delete_file(file_path):
    os.remove(file_path)
    dir_of_file = os.path.split(file_path)[0]
    print(dir_of_file)
    if len(os.listdir(dir_of_file)) == 0:
        os.rmdir(dir_of_file)


@app.route('/<inp_hash>', methods=['DELETE', 'GET'])
def hash_path_action(inp_hash):
    if not re.match(r'^[0-9a-f]{32}$', inp_hash):
        return 'The request does not contain an MD5 checksum', 400
    file_path = get_result_path(UPLOAD_FOLDER, inp_hash)
    if not os.path.exists(file_path):
        return 'No file with such a checksum was found', 404
    if request.method == 'GET':
        return send_file(file_path, mimetype='application/octet-stream')
    if request.method == 'DELETE':
        delete_file(file_path)
        return '', 200


@app.route('/', methods=['POST'])
def root_path_action():
    if request.method == 'POST':
        data = request.get_data(cache=False, as_text=False, parse_form_data=False)
        hash_file = hashlib.md5(data).hexdigest()
        create_folder(UPLOAD_FOLDER, hash_file)
        with open(get_result_path(UPLOAD_FOLDER, hash_file), 'wb+') as f:
            f.write(data)
        return '', 200, {'Hash_of_file': hash_file}


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
