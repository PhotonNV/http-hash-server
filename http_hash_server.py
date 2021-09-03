from flask import Flask, request, send_file
import hashlib
import os
import re

UPLOAD_FOLDER = '/home/aramzaev/pr_test/'
app = Flask(__name__)


def get_rezult_dir (upload_folder, hash):
    return upload_folder+hash[0:2]+'/'

def  get_rezult_path (upload_folder, hash):
    return get_rezult_dir (upload_folder, hash) + hash

def create_folder(upload_folder, hash):
    result_dir = get_rezult_dir(upload_folder, hash)
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    return result_dir

def delete_file(file_path):
    os.remove(file_path)
    dir_of_file = re.sub(r'/' + file_path.split('/')[-1] + '$', '', file_path)
    if len(os.listdir(dir_of_file)) == 0:
        os.rmdir(dir_of_file)

@app.route('/<hash>', methods = ['DELETE', 'GET'])
def hash_path_action(hash):
    if not re.match(r'^[0-9a-f]{32}$', hash):
        return '', 400
    file_path = get_rezult_path(UPLOAD_FOLDER, hash)
    if not os.path.exists(file_path):
        return '', 404
    if request.method == 'GET':
        return send_file(file_path, mimetype='application/octet-stream')
    if request.method == 'DELETE':
        delete_file(file_path)
        return '', 200



@app.route('/', methods = ['PUT'])
def root_path_action():
    if request.method == 'PUT':
        data = request.get_data(cache=False, as_text=False, parse_form_data=False)
        hash_file = hashlib.md5(data).hexdigest()
        create_folder(UPLOAD_FOLDER, hash_file)
        with open(get_rezult_path(UPLOAD_FOLDER, hash_file), 'wb+') as f:
            f.write(data)
        return '',200,{'Hash_of_file': hash_file}


if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True)
    app.run(debug=True)