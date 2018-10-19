# BENCHOP as a Service

## Install Docker on the VM

    sudo apt-get install -y docker-ce
    

### App Container


### Broker Container

  Navigate to acc-project/baas/broker
  
  Requires Dockerfile

  run: 
  
    sudo docker build -t broker . 
    
    sudo docker run broker

### Worker Containers
