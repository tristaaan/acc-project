#!/bin/bash
docker pull rabbitmq
docker run --rm -d --hostname my-rabbit -e RABBITMQ_DEFAULT_USER=ubuntu -e RABBITMQ_DEFAULT_PASS=1234 -e RABBITMQ_DEFAULT_VHOST=myvhost rabbitmq:3

