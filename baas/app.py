#!/usr/bin/python
import subprocess
import sys
from flask import Flask, jsonify
from flasgger import Swagger

import sys
# hack, sorry PEP8
sys.path.insert(0, "/home/ubuntu/acc-project/worker")
from tasks import test_method

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

@app.route('/problem/<string:name>', methods=['POST'])
def parameter_problem(name):
  '''
  Run a problem
  ---
  tags:
    - problems
  parameters:
    - name: name
      in: path
      type: string
      required: true
      description: The name of the problem
    - name: body
      in: body
      required:
        - S
        - K
        - T
        - r
        - sig
      schema:
        id: param_query
        required:
          - candidate_id
          - context
        properties:
          S:
            type: float
            description: Initial asset price
            example: 90
          K:
            type: float
            description: Strike price
            example: 100
          T:
            type: float
            description: Terminal time
            example: 1.0
          r:
            type: float
            description: Risk-free interest rate
            example: 0.03
          sig:
            type: float
            description: Volatility
            example: 0.15
  responses:
    200:
      description: Results
    404:
      description: Problem not found
  '''
  return 'Problem "%s" requested' % name

@app.route('/problem/test', methods=['GET'])
def test_method():
    tm = test_method.delay()
    return tm.wait()

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
