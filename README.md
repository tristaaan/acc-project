# BENCHOP as a Service

## Install Docker on the VM (Community Edition)

    sudo apt-get update
    
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    
    sudo apt-get install -y docker-ce
    

### a.  BaaS-App Container

  Navigate to acc-project/baas (requires Dockerfile inside)

  run: 
  
    sudo docker build -t baas . 
    
    sudo docker run baas



### b.  Broker Container

  Navigate to acc-project/broker (requires Dockerfile inside)

  run: 
  
    sudo docker build -t broker . 
    
    sudo docker run broker


### c.  Worker Containers

Navigate to acc-project/worker (requires Dockerfile inside)

  run: 
  
    sudo docker build -t worker<Nr> . 
    
    sudo docker run worker<Nr>
