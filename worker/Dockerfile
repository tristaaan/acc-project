FROM ubuntu
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y octave
RUN apt-get install -y wget
RUN apt-get install -y python-dev python-pip
RUN pip install celery
RUN pip install oct2py
RUN pip install numpy
RUN pip install scipy
WORKDIR /home/ubuntu
ADD . ./
CMD celery worker -A tasks --loglevel=info
