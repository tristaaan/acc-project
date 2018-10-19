FROM ubuntu
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python-pip
RUN pip install --upgrade pip
RUN apt-get install -y rabbitmq-server
ADD brokerConfig.sh ./
EXPOSE 5000

CMD ["bash", "brokerConfig.sh"]
