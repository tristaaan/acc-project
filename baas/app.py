#!/usr/bin/python
import json
import requests
import os
import subprocess
import sys
from flask import Flask, abort, jsonify, request
from flasgger import Swagger
from celery import group
from werkzeug.utils import secure_filename

# hacky import, sorry PEP8
sys.path.insert(0, "/home/ubuntu/acc-project/worker")
import tasks

# File upload support
UPLOAD_FOLDER = '/home/ubuntu/uploads'
ALLOWED_EXTENSIONS = set(['zip'])
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

my_key ='acc-group13'
private_key = subprocess.check_output(['cat', '/home/ubuntu/.ssh/%s' % my_key]).decode()

#methods={'MC','MC-S','QMC-S','MLMC','MLMC-A','FFT','FGL','COS','FD',
#    'FD-NU','FD-AD','RBF','RBF-FD','RBF-PUM','RBF-LSML','RBF-AD','RBF-MLT'};

methods = ['MC-S','QMC-S','MLMC','MLMC-A','FFT','FGL','COS','FD',
    'FD-NU','FD-AD','RBF','RBF-FD','RBF-PUM','RBF-LSML','RBF-AD','RBF-MLT']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Swagger(app, template={
    "info": {
        "title": "BENCHOP as a Service API",
        "version": "0.6",
    }
})

# all_problems = ['problem1_A1', 'problem1_A2', 'problem1_B1', 'problem1_B2', 'problem1_C1', 'problem1_C2']
all_problems = ['problem1_A1', 'problem1_B1', 'problem1_B2', 'problem1_C1']

@app.route('/problem/all', methods=['GET'])
def all():
    """
    Run all benchmarks
    ---
    tags:
        - problems
    responses:
        500:
            description: There was some error
        200:
            description: The results of the benchmark
    """
    stats = []
    for p in all_problems:
        stats.append(tasks.compute.s(p))
    results = group(stats).apply_async() \
        .get(timeout=600)
    return json.dumps(results)

@app.route('/problem/<string:name>', methods=['GET'])
def problem(name):
    '''
    Run a simple test problem given some parameters
    ---
    tags:
        - problems
    parameters:
        - name: name
          in: path
          type: string
          required: true
          description: The name of the problem
        - name: S
          in: query
          type: float
          description: Initial asset price
          example: 90
        - name: K
          in: query
          type: float
          description: Strike price
          example: 100
        - name: T
          in: query
          type: float
          description: Terminal time
          example: 1.0
        - name: r
          in: query
          type: float
          description: Risk-free interest rate
          example: 0.03
        - name: sig
          in: query
          type: float
          description: Volatility
          example: 0.15
    responses:
        200:
            description: Results
        400:
            description: Incomplete parameters
        404:
            description: Problem not found
    '''
    if 'S' in request.args or 'K' in request.args or \
        'T' in request.args or 'r' in request.args or 'sig' in request.args:
        tm, rel = tasks.compute_param.delay(name, methods, request.args)
    else:
        tm, rel = tasks.compute.delay(name).get()
    return str(tm) + ' ' + str(rel)

@app.route('/problem/test', methods=['GET'])
def run_test_method():
    '''
    Run a problem
    ---
    tags:
        - problems
    parameters:
        - name: a
          in: query
          required: true
          type: number
          example: 2
        - name: b
          in: query
          required: true
          type: number
          example: 3
        - name: c
          in: query
          required: true
          type: number
          example: 4
    responses:
        200:
            description: Result of `(a + b) * c`
        400:
            description: Invalid parameters
    '''
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    c = int(request.args.get('c'))
    tm = tasks.test_method_param.delay(a, b, c)
    return str(tm.wait())

@app.route('/problems/upload', methods=['POST'])
def upload_method():
    '''
    Upload a new method
    ---
    tags:
        - problems
    parameters:
      - in: formData
        type: file
        name: file
        required: true
        description: Upload your file in a zip.
    responses:
        200:
            description: File uploaded
    '''
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        abort(400)
    file = request.files['file']
    # if user does not select file
    if file.filename == '':
        flash('No selected file')
        abort(400)
    # save file to the upload folder, tell the workers to fetch it
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        r = tasks.upload_zip.delay(file_path, private_key)
        return r.wait()
    abort(501)
    return 1

@app.route('/workers', methods=['GET'])
def get_workers():
    """
    Get a list of available workers.
    ---
    tags:
        - workers
    responses:
        200:
            description: JSON of the workers and their statuses
    """
    r = requests.get('http://localhost:5555/api/workers?status=online')
    return json.dumps(r.json(), indent=2)

@app.route('/workers/methods', methods=['GET'])
def get_worker_methods():
    """
    Get a list of available methods.
    ---
    tags:
        - workers
    responses:
        200:
            description: Array of methods
    """
    r = tasks.available_methods.delay()
    return json.dumps(r.wait())

@app.route('/version', methods=['GET'])
def version():
    """
    Get octave version
    ---
    tags:
        - workers
    responses:
        200:
            description: version of octave
    """
    r = tasks.version.delay()
    return r.wait()

# consult rabbitmq manager api:
# https://cdn.rawgit.com/rabbitmq/rabbitmq-management/v3.7.8/priv/www/api/index.html
@app.route('/queue', methods=['GET'])
def get_queue():
    """
    inspect messages in the queue
    ---
    tags:
        - queue
    responses:
        200:
            description: queue
    """
    headers = { 'content-type': 'application/json' }
    auth = ('ubuntu', '1234')
    data = json.dumps({
        'count':5, 'ackmode':'reject_requeue_true', 'encoding':'auto'
    })
    r = requests.post('http://localhost:15672/api/queues/myvhost/default/get', \
        auth=auth, headers=headers, data=data)
    return json.dumps(r.json(), indent=2)

@app.route('/queue', methods=['DELETE'])
def purge_queue():
    """
    purge messages in the queue
    ---
    tags:
        - queue
    responses:
        200:
            description: queue
    """
    auth = ('ubuntu', '1234')
    r = requests.delete('http://localhost:15672/api/queues/myvhost/default/contents', \
        auth=auth)
    return 'Queue cleared'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
