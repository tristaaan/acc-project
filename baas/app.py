#!/usr/bin/python
import json
import requests
import subprocess
import sys
from flask import Flask, jsonify, request
from flasgger import Swagger
from celery import group

# hacky import, sorry PEP8
sys.path.insert(0, "/home/ubuntu/acc-project/worker")
import tasks

UPLOAD_FOLDER = '~/problem_uploads/'
ALLOWED_EXTENSIONS = set(['m', 'mat'])

#meths={'MC','MC-S','QMC-S','MLMC','MLMC-A','FFT','FGL','COS','FD',
#    'FD-NU','FD-AD','RBF','RBF-FD','RBF-PUM','RBF-LSML','RBF-AD','RBF-MLT'};

meths=['MC-S','QMC-S','MLMC','MLMC-A','FFT','FGL','COS','FD',
'FD-NU','FD-AD','RBF','RBF-FD','RBF-PUM','RBF-LSML','RBF-AD','RBF-MLT']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Swagger(app, template={
    "info": {
        "title": "BENCHOP as a Service API",
        "version": "0.6",
    }
})

all_problems = ['problem1_A1', 'problem1_A2', 'problem1_B1', 'problem1_B2', 'problem1_C1', 'problem1_C2']

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
    results = group(stats).apply_async().get()
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
        tm, rel = tasks.compute_param.delay(name, meths, request.args)
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
          type: string
          example: 2
        - name: b
          in: query
          required: true
          type: string
          example: 3
        - name: c
          in: query
          required: true
          type: string
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

@app.route('/upload_method', methods=['GET'])
def upload_method(name, file):
    '''
    Upload a method
    ---
    tags:
        - problems
    parameters:
        - name: method tag
          in: query
          required: true
          type: string
          example: MC
        - name: method file
          in: formData
          required: true
          type: file
    responses:
        200:
            description: File uploaded
        400:
            description: Invalid parameters
    '''
    #save file in UPLOAD_FOLDER
    file.
    meths.append(name)
    #copy method file into every worker via broadcast task
    # ...
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
    r = requests.get('http://localhost:5555/api/workers?status')
    return json.dumps(r.json(), indent=2)

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
    return tasks.version()

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
