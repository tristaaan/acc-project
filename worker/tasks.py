from __future__ import absolute_import
from .celery import app
from oct2py import Oct2Py

@app.task
def compute(problemname):
    oc = Oct2Py()
    time, relerr = oc.feval(problemname)
    timelist = time.tolist()
    relerrlist = relerr.tolist()
    return timelist, relerrlist

@app.task
def compute_par(problemname, parameters):
    oc = Oct2Py()
    time, relerr = oc.feval(problemname + "_param", 
                            parameters.get("S"), parameters.get("K"), parameters.get("T"), 
                            parameters.get("r"), parameters.get("sig"), parameters.get("U"), -1)
    timelist = time.tolist()
    relerrlist = relerr.tolist()
    return timelist, relerrlist

@app.task
def test_method():
    oc = Oct2Py()
    res = oc.feval(3,4,10)
    return res

@app.task
def test_method_param(x,y,z):
    oc = Oct2Py()
    res = oc.feval(x,y,z)
    return res

@app.task
def test_method_param_list(params):
    oc = Oct2Py()
    res = oc.feval(params[0], params[1], params[2])
    return res