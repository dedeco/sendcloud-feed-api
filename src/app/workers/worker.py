from celery import Celery

celery_app = Celery(
    "worker",
    backend="redis://redis:6379/0",
    broker="amqp://rabbitmq:5672//"
)

celery_app.autodiscover_tasks(packages=['app.workers.entries'])