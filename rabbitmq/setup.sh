#!/bin/bash
docker pull rabbitmq
docker run --rm -d --hostname my-rabbit --name my_rabbit \
  -e RABBITMQ_DEFAULT_USER=ubuntu -e RABBITMQ_DEFAULT_PASS=1234 \
  -e RABBITMQ_DEFAULT_VHOST=myvhost -p 5672:5672 -p 15672:15672 \
  rabbitmq:3-management
