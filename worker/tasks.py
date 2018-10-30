from oct2py import Oct2Py, utils
from celery import Celery

baas_broker = 'amqp://ubuntu:1234@192.168.1.75:5672/myvhost'
baas_backend = 'amqp://ubuntu:1234@192.168.1.75:5672/myvhost'
app = Celery('celery_app', broker=baas_broker, backend=baas_backend)

# change directory to BENCHOP and return the Oct2Py object
def config():
    oc = Oct2Py()
    oc.chdir('BENCHOP/')
    return oc

@app.task
def compute(problemname):
    oc = config()
    time, relerr = oc.feval(problemname, nout=2)
    timelist = time.tolist()
    relerrlist = relerr.tolist()
    return (timelist, relerrlist)

@app.task
def compute_param(problemname, parameters):
    oc = config()
    time, relerr = oc.feval(problemname + "_param",
                            parameters.get("S"), parameters.get("K"), parameters.get("T"),
                            parameters.get("r"), parameters.get("sig"), parameters.get("U"), -1,
                            nout=2)
    timelist = time.tolist()
    relerrlist = relerr.tolist()
    return timelist, relerrlist

@app.task
def test_method_param(x,y,z):
    oc = config()
    res = oc.feval('test_function', x, y, z)
    return res

@app.task
def version():
    return utils.sys.version
