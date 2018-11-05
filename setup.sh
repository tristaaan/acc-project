#!/bin/bash
# To be run on a fresh instance

# Install prerequisites
sudo apt-get install docker.io octave
alias python=python3
alias pip=pip3

# install all the python
pip install -r requirements.txt

export WORKER_NAME=acc_worker
export MANAGER_IP=$(ifconfig -a | sed -En 's/.*inet addr:(192.168.[0-9]+.[0-9]+).*/\1/p')

# run the api
python baas/app.py &

# prepare queue and worker inspection
sudo rabbitmq/setup.sh
sudo flower/setup.sh

# get the worker image, create a swarm
sudo docker pull tristaaan/acc-worker
sudo docker swarm init
sudo docker service create --name workers tristaaan/acc-worker:latest \
  -e MANAGER_IP=${MANAGER_IP}

# Do not put workers on the manager node
MANAGER_ID=$(sudo docker node ls -f "role=manager" --format "{{.ID}}")
docker node update --availability drain ${MANAGER_ID}

echo 'ready to scale: sudo docker service scale workers=#'
if [-z ${OS_USER_DOMAIN_NAME+x}]; then
  echo OpenStack credentials unset, you won't be able to spawn nodes.
else
  echo create nodes  : python context/spawn-node.py
fi
