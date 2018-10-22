from __future__ import absolute_import
from celery import Celery

baas_broker = 'amqp://acc13_user:acc13_pw@localhost/acc13_vhost'

app = Celery('baas',
             broker= baas_broker,
             backend= baas_broker,
             include=['.tasks'])


if __name__ == '__main__': 
    app.start()