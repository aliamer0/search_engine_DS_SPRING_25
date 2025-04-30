from task_queue import app

@app.task
def distribute_url(url):
    print(f"Received URL: {url}")
