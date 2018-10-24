from celery import Celery

baas_broker = 'amqp://ubuntu:1234@192.168.1.75:5672/myvhost'
# baas_backend = 'amqp://ubuntu:1234@my-rabbit:5672/myvhost'
app = Celery('celery_app', broker=baas_broker)

@app.task
def add(x, y):
	return x + y
