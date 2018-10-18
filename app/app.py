#!flask/bin/python
from flask import Flask, jsonify
from flasgger import Swagger
import subprocess
import sys

app = Flask(__name__)
Swagger(app)

@app.route('/methods/all', methods=['GET'])
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
  data=subprocess.check_output(['octave', '--version'])
  return 'unimplemented'

@app.route('/methods/version', methods=['GET'])
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