#!/bin/bash
IP=$(ifconfig -a | sed -En 's/.*inet addr:(192.168.[0-9]+.[0-9]+).*/\1/p')
docker pull iserko/docker-celery-flower
docker run --rm -d -p 5555:5555 \
  -e CELERY_BROKER_URL=amqp://ubuntu:1234@${IP}:5672/myvhost \
  iserko/docker-celery-flower --broker_api=http://ubuntu:1234@${IP}:5672/myvhost \
  --persistent=False
