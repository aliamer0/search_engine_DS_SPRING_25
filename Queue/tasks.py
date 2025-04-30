from task_queue import app

@app.task(queue= 'urls')
def distribute_url(url):
    print(f"Received URL: {url}")
