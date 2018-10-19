#!/bin/bash
rabbitmq-server start
rabbitmqctl add_user acc13_user acc13_pw
rabbitmqctl add_vhost acc13_vhost
rabbitmqctl set_permissions -p acc13_vhost acc13_user ".*" ".*" ".*"
rabbitmqctl set_user_tags acc13_user administrator
rabbitmq-plugins enable rabbitmq_management
