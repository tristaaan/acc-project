#!flask/bin/python
from flask import Flask, jsonify
from flasgger import Swagger
import subprocess
import sys

app = Flask(__name__)
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
  responses:
    500:
      description: Error The language is not awesome!
    200:
      description: the results of the benchmark
  """
  return 'unimplemented'

@app.route('/problem/<string:name>', methods=['POST'])
def fd(name):
  '''
  Run a problem
  ---
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
  '''
  return 'Problem "%s" requested' % name

# @app.route('/problem/', methods=['POST'])
# def rbf_fd():
#   return 'unimplemented'

# @app.route('/problem/', methods=['POST'])
# def cos():
#   return 'unimplemented'

@app.route('/version', methods=['GET'])
def version():
  """
  Get octave version
  ---
  responses:
    200:
      description: version of octave
  """
  return subprocess.check_output(['octave', '--version'])

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)