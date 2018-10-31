from oct2py import Oct2Py, utils
from celery import Celery
import subprocess
import sys
import zipfile

baas_broker = 'amqp://ubuntu:1234@192.168.1.75:5672/myvhost'
baas_backend = 'amqp://ubuntu:1234@192.168.1.75:5672/myvhost'
app = Celery('celery_app', broker=baas_broker, backend=baas_backend)

# change directory to BENCHOP and return the Oct2Py object
def config():
    oc = Oct2Py()
    oc.chdir('BENCHOP/')
    return oc

@app.task
def pull_method(name, zip_string):
    #command = "scp -r %s:/UPLOAD_FOLDER/%s DESTINATION/BENCHOP/" % (origin, name)
    #out = subprocess.check_output(command.split(" ")) #split?

    # save file
    zip_name = name + '.zip'
    with open(zip_name, 'w') as file:
        file.write(zip_string)
    # extract file
    with zipfile.ZipFile('newmethod.zip', "r") as z:
        z.extractall("/home/ubuntu/BENCHOP/%s" % (name)) #zip.split('.')[0]))
    return 1

@app.task
def compute(problemname, methods):
    oc = config()
    time, relerr = oc.feval(problemname, methods, nout=2)
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
