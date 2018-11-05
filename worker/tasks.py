import os, subprocess, sys, zipfile

from oct2py import Oct2Py, utils
from celery import Celery
from kombu import Queue
from kombu.common import Broadcast

manager_ip = os.getenv('MANAGER_IP', '192.168.1.7')

baas_broker = 'amqp://ubuntu:1234@%s:5672/myvhost' % manager_ip
baas_backend = 'amqp://ubuntu:1234@%s:5672/myvhost' % manager_ip
app = Celery('celery_app', broker=baas_broker, backend=baas_backend)
app.conf.task_queues = (Queue('default'), Broadcast('broadcast_tasks'),)

UPLOAD_FOLDER = '/home/ubuntu/worker_uploads'
BENCHOP_FOLDER = '/home/ubuntu/BENCHOP'

# change directory to BENCHOP and return the Oct2Py object
def config():
    oc = Oct2Py()
    oc.chdir('BENCHOP/')
    return oc

@app.task(queue='broadcast_tasks')
def upload_zip(method_path, private_key):
    # install key, if necessary
    private_path = '/home/ubuntu/private'
    if not os.path.isfile(private_path):
        with open(private_path, 'w') as file:
            file.write(private_key)
        subprocess.check_output(('chmod 600 %s' % private_path).split(' '))

    # create the upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # scp target zip file to the upload folder
    subprocess.check_output(('scp -o StrictHostKeyChecking=no -i %s ubuntu@%s:%s %s/.' %
        (private_path, manager_ip, method_path, UPLOAD_FOLDER)).split(' '))

    # extract file to benchop
    filename = method_path.split('/')[-1]
    name = filename.split('.')[0]
    with zipfile.ZipFile('%s/%s' % (UPLOAD_FOLDER, filename), "r") as z:
        z.extractall("%s/%s" % (BENCHOP_FOLDER, name))
    return 'uploaded and distributed file %s' % filename

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

@app.task(queue='default')
def version():
    return utils.sys.version

@app.task(queue='default')
def available_methods():
    methods = [x[0].split('/')[-1] for x in os.walk('/home/ubuntu/BENCHOP/')]
    return list(filter(lambda x: len(x) > 1, methods))
