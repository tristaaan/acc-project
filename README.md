# BENCHOP as a Service

## Idea

Select a problem, and optional set parameters, to request a solution from BenchOp. The request is received by the baas application and creates a queue for the broker to distribute the tasks to the workers. Each workers will return its result and the baas application connects them into a ranking/statistic which is finally shown to the end-user. The whole process is observed by Flower to check the progress.


## Make it work

### Start a VM

Go to https://uppmax.cloud.snic.se/project/instances/ and set up an instance with the following settings: 

    Name: ACC15_BENCHOP
    
    Size: ACCHT18.normal
    
    Key Pair: group-13
    
    Network: SNIC 2018/10-30 Internal IPv4 Network
    
    Security Groups: gpl
    
+ assign Floating-IP ! (atm 130.238.28.220)
[maybe as CloudInit]

### Prepare the VM 

[maybe as cloud-config]

Install Docker on the VM (Community Edition):

    sudo apt-get update
    
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    
    sudo apt-get install -y docker-ce

Clone the Github repository 
    
    git clone https://github.com/tristaaan/acc-project.git


### a.  BaaS-App Container

#### Info

  + The BenchOp-as-a-Service-App allows HTTP-requests to request results for BenchOp functions and given parameters.
  + The Dockerfile imports Flask, Swagger(?), ...

#### Use it
Navigate to acc-project/baas (requires Dockerfile inside) and start the container:
  
    sudo docker build -t baas . 
    
    sudo docker run baas


### b.  Broker Container

#### Info

  + The broker distributes tasks to the workers using a queue.
  + The Dockerfile imports the rabbitmq-server and sets up a user and the user-settings.

#### Use it
Navigate to acc-project/broker (requires Dockerfile inside) and start the container:
  
    sudo docker build -t broker . 
    
    sudo docker run broker


### c.  Worker Containers

#### Info

  + Each worker has its own container. It receives a task from the broker to compute it and returns a result. 
  + The Dockerfile imports the BenchOp functions, octave, celery and connect the worker to the broker.

#### Use it
Navigate to acc-project/worker (requires Dockerfile inside) and start the container:

    sudo docker build -t worker<Nr> . 
    
    sudo docker run worker<Nr>


### d.  (Flower Container ?)

#### Info

  + A tool to control the workers. Use with URL in the browser to get a UI.
  + (automatically connects to all rabbitmq traffic / broker ?)

#### Use it
Navigate to acc-project/flower (requires Dockerfile inside) and start the container: 
  
    sudo docker build -t flower . 
    
    sudo docker run flower
    

### e.  (User Interface ?)

#### Info

  + ...

#### Use it
  
...

    ...
