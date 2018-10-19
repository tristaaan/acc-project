# BENCHOP as a Service

## Install Docker on the VM

    sudo apt-get update
    
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    
    sudo apt-get install -y docker-ce
    

### I.      App Container


### II.     Broker Container

  Navigate to acc-project/baas/broker
  
  Requires Dockerfile

  run: 
  
    sudo docker build -t broker . 
    
    sudo docker run broker

### III.    Worker Containers
