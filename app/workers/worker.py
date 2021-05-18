from celery import Celery

celery_app = Celery(
    "worker",
    backend="redis://localhost:6379/0",
    broker="amqp://localhost:5672//"
)

celery_app.autodiscover_tasks(packages=['app.workers.entries'])