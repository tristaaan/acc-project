# BENCHOP as a Service

## Install Docker on the VM (Community Edition)

    sudo apt-get update
    
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    
    sudo apt-get install -y docker-ce
    

### a.  App Container


### b.  Broker Container

  Navigate to acc-project/baas/broker (requires Dockerfile inside)

  run: 
  
    sudo docker build -t broker . 
    
    sudo docker run broker

### c.  Worker Containers
