import subprocess
import sys
import zipfile

from oct2py import Oct2Py, utils
from celery import Celery
from kombu import Queue
from kombu.common import Broadcast

baas_broker = 'amqp://ubuntu:1234@192.168.1.75:5672/myvhost'
baas_backend = 'amqp://ubuntu:1234@192.168.1.75:5672/myvhost'
app = Celery('celery_app', broker=baas_broker, backend=baas_backend)

app.conf.task_queues = (Queue('default'), Broadcast('broadcast_tasks'),)

# change directory to BENCHOP and return the Oct2Py object
def config():
    oc = Oct2Py()
    oc.chdir('BENCHOP/')
    return oc

@app.task(queue='broadcast_tasks')
def upload_zip(filename, zip_string):
    # save file
    with open(filename, 'wb') as file:
        file.write(zip_string)
    # extract file
    name = filename.split('.')[0]
    with zipfile.ZipFile(filename, "r") as z:
        z.extractall("/home/ubuntu/BENCHOP/%s" % (name)) #zip.split('.')[0]))
    return 1

@app.task(queue='default')
def compute(problemname):
    oc = config()
    time, relerr = oc.feval(problemname, nout=2)
    timelist = time.tolist()
    relerrlist = relerr.tolist()
    return (timelist, relerrlist)

@app.task(queue='default')
def compute_param(problemname, parameters):
    oc = config()
    time, relerr = oc.feval(problemname + "_param",
                            parameters.get("S"), parameters.get("K"), parameters.get("T"),
                            parameters.get("r"), parameters.get("sig"), parameters.get("U"), -1,
                            nout=2)
    timelist = time.tolist()
    relerrlist = relerr.tolist()
    return timelist, relerrlist

@app.task(queue='default')
def test_method_param(x,y,z):
    oc = config()
    res = oc.feval('test_function', x, y, z)
    return res

@app.task
def version():
    return utils.sys.version
