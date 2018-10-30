# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, re, inspect

from os import environ as env
from random import randint
from string import Template
from subprocess import check_output

from novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

flavor = "ACCHT18.normal"
private_net = 'SNIC 2018/10-30 Internal IPv4 Network'
floating_ip_pool_name = None
floating_ip = ''
image_name = 'Ubuntu 16.04 LTS (Xenial Xerus) - latest'

loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_name=env['OS_USER_DOMAIN_NAME'],
                                project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print("user authorization completed.")

image = nova.glance.find_image(image_name)
flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

# Confire template information for cloud-init script
my_key ='acc-group13'
template_data = {}
# template_data['public_key'] = check_output(['cat', '/home/ubuntu/.ssh/%s.pub' % my_key]).decode()
# template_data['private_key'] = check_output(['cat', '/home/ubuntu/.ssh/%s' % my_key]) \
#     .decode() \
#     .replace('\n', '\n      ') # yaml indentation!
# strip the stray newline from the swarm token
template_data['docker_token'] = check_output(\
    'sudo docker swarm join-token worker -q'.split(' ')).decode().strip()
# local machine ip
template_data['ip'] = re.findall(r'192\.168\.\d+\.\d+', \
    check_output(['ifconfig', '-a']).decode())[0]

# names of template and init script
template_name = 'node_init_template.yml'

# open template, sub in parameters
userfile = open(template_name, 'r')
userdata_str = Template(userfile.read()).substitute(template_data)

secgroups = ['default', 'gpl', 'celery']

id = randint(1,256)
print('Creating instance ... %d' % id)
instance = nova.servers.create(name="acc13-worker-%d" % id, image=image, flavor=flavor, userdata=userdata_str, \
                               nics=nics,security_groups=secgroups, key_name='group-13')
inst_status = instance.status
print("waiting for 10 seconds.. ")
time.sleep(10)

while inst_status == 'BUILD':
    print("Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more...")
    time.sleep(5)
    instance = nova.servers.get(instance.id)
    inst_status = instance.status

print("Instance: "+ instance.name +" is in " + inst_status + "state " + instance.accessIPv4)
