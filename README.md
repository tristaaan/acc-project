# BENCHOP as a Service


## Getting started

Setup a new VM with docker, clone the repository, `cd` to the folder, and run `setup.sh`:

```
git clone https://github.com/tristaaan/acc-project.git
cd acc-projcet
sudo setup.sh
```

This will install apt-libraries, some required python libraries, and spawn the RabbitMQ and Flower containers. It will also initialize and setup a docker swarm which runs the worker container.

## Usage

### API

If the the root `setup.sh` was run without errors the API should be running on port 5000. Navigating to the proper URL will take you to the API interface where you can manually query the API or retrieve curl calls which do the same thing.

### Scaling

It is up to the user to spawn more nodes and scale the service. This can be done respectively with:

```sh
# create a new node, OpenStack credentials required.
python context/spawn-node.py
# spawn two worker containers on the swarm
sudo docker service scale workers=2
```

Note that the new node might not be immediately available and ready, check with:

```sh
docker node ls
```
