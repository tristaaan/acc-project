# BENCHOP as a Service

## 

## Idea

## Use it

### Start a VM

Go to https://uppmax.cloud.snic.se/project/instances/ and set up an instance with the following settings:
    
    Name: ACC15_BENCHOP
    
    Size: ACCHT18.normal
    
    Key Pair: group-13
    
    Network: SNIC 2018/10-30 Internal IPv4 Network
    
    Security Groups: gpl
    
  + assign Floating-IP ! (atm 130.238.28.220)


### Preparation

Install Docker on the VM (Community Edition):

    sudo apt-get update
    
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    
    sudo apt-get install -y docker-ce
    

### a.  BaaS-App Container

#### Info

#### Use it
  Navigate to acc-project/baas (requires Dockerfile inside) and start the container:
  
    sudo docker build -t baas . 
    
    sudo docker run baas



### b.  Broker Container

#### Info

#### Use it
  Navigate to acc-project/broker (requires Dockerfile inside) and start the container:
  
    sudo docker build -t broker . 
    
    sudo docker run broker


### c.  Worker Containers

#### Info

#### Use it
Navigate to acc-project/worker (requires Dockerfile inside) and start the container:

    sudo docker build -t worker<Nr> . 
    
    sudo docker run worker<Nr>


### d.  (Flower Container ?)

#### Info

#### Use it
Navigate to acc-project/flower (requires Dockerfile inside) and start the container: 
  
    sudo docker build -t flower . 
    
    sudo docker run flower
