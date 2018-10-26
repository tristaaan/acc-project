#!/usr/bin/python
import subprocess
import sys
from flask import Flask, jsonify, request
from flasgger import Swagger

import sys
# hack, sorry PEP8
sys.path.insert(0, "/home/ubuntu/acc-project/worker")
from tasks import test_method_param, compute, compute_param

UPLOAD_FOLDER = '~/problem_uploads/'
ALLOWED_EXTENSIONS = set(['m', 'mat'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Swagger(app, template={
  "info": {
    "title": "BENCHOP as a Service API",
    "version": "0.5",
  }
})

@app.route('/problem/all', methods=['GET'])
def all():
  """
  Run all benchmarks
  ---
  tags:
    - problems
  responses:
    500:
      description: Error The language is not awesome!
    200:
      description: the results of the benchmark
  """
  return 'unimplemented'

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
    - S:
      in: query
      type: float
      description: Initial asset price
      example: 90
    - K:
      in: query
      type: float
      description: Strike price
      example: 100
    - T:
      type: float
      description: Terminal time
      example: 1.0
    - r:
      type: float
      description: Risk-free interest rate
      example: 0.03
    - sig:
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
    tm = compute_param.delay(name, request.args)
  else:
    tm = compute.delay(name)
  return 'Problem "%s" requested' % name

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
    tm = test_method_param.delay(a, b, c)
    return str(tm.wait())

@app.route('/version', methods=['GET'])
def version():
  """
  Get octave version
  ---
  tags:
    - meta
  responses:
    200:
      description: version of octave
  """
  return subprocess.check_output(['octave', '--version'])

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)
