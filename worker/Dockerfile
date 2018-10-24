FROM ubuntu
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python-pip
RUN pip install --upgrade pip
RUN pip install celery
WORKDIR /home/ubuntu
ADD /home/ubuntu/acc-project/worker worker/
CMD celery worker -A tasks --loglevel=info
