from celery import shared_task
from main.sheduler import send_subscribtions


@shared_task
def add(x, y):
    return x + y


@shared_task
def task_subscription():
    send_subscribtions()   