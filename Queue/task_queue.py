from celery import Celery

# Configure Celery
app = Celery('Search Engine',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/1',
             include=['Queue.tasks'])

# Optional configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,
    task_soft_time_limit=240,
    worker_max_tasks_per_child=100,
    task_acks_late=True,
    broker_transport_options={'visibility_timeout': 3600},
)
