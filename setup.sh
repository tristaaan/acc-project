#!/bin/bash
# install all the python stuff
pip install -r requirements

# prepare queue and worker inspection
sudo rabbitmq/setup.sh
sudo flower/setup.sh

# get the worker image, create a swarm
sudo docker pull tristaaan/acc-worker
sudo docker swarm init
sudo docker service create --name workers tristaaan/acc-worker

echo 'ready to scale: sudo docker service scale workers=#'
echo 'create nodes  : python context/spawn-node.py'
