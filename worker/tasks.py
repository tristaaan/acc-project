from __future__ import absolute_import
from celery import app

@app.task
def plus(x, y):
    return x + y

@app.task
def minus(x, y):
    return x - y