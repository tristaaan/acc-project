#!/bin/bash
docker pull iserko/docker-celery-flower
docker run --rm -d -p 5555:5555 \
  -e CELERY_BROKER_URL=amqp://ubuntu:1234@192.168.1.75:5672/myvhost \
  iserko/docker-celery-flower --broker_api=http://ubuntu:1234@192.168.1.75:5672/myvhost \
  --persistent=False
