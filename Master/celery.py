from celery import Celery

app = Celery('_queue', backend = 'redis://localhost:6379/0', broker='redis://localhost:6379/0')
app.config_from_object('celeryconfig')

@app.task
def add(x, y):
    return x + y
