#!/bin/bash
# To be run on a fresh instance, use sudo

# Install prerequisites
apt-get install -y docker.io octave python-dev python-pip
alias python=python3
alias pip=pip3

# install all the python
pip install -r requirements.txt

export WORKER_NAME=acc_worker
export MANAGER_IP=$(ifconfig -a | sed -En 's/.*inet addr:(192.168.[0-9]+.[0-9]+).*/\1/p')

# run the api
python baas/app.py &

# start the queue and worker inspection tool
rabbitmq/setup.sh
flower/setup.sh

# get the worker image, create a swarm
docker pull tristaaan/acc-worker
docker swarm init
docker swarm update --task-history-limit 1
docker service create --name workers tristaaan/acc-worker:latest \
  -e MANAGER_IP=${MANAGER_IP}

# Do not put workers on the manager node
MANAGER_ID=$(docker node ls -f "role=manager" --format "{{.ID}}")
docker node update --availability drain ${MANAGER_ID}

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

printf '${GREEN}ready to scale: sudo docker service scale workers=#${NC}\n'
if [[ -z ${OS_USER_DOMAIN_NAME+x} ]]; then
  printf "${RED}OpenStack credentials unset, you won't be able to spawn nodes.${NC}\n"
else
  printf "create nodes  : python context/spawn-node.py\n"
fi
