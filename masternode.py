import queue
import threading
import time
from queue import Queue
from indexer import add_document  # Import add_document function from indexer.py

# Simulate a task queue for URLs to crawl
task_queue = Queue()
data_queue = Queue()  # Queue to hold crawled data for the indexer

# List of seed URLs (normally this could be loaded from a file or database)
seed_urls = [
    "https://en.wikipedia.org/wiki/SS_Normandie",
    "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "https://en.wikipedia.org/wiki/Web_crawler"
]

# Load seed URLs into the task queue
def load_seed_urls():
    for url in seed_urls:
        task_queue.put(url)
        print(f"[Master] Seed URL added to queue: {url}")

# Simulate sending tasks to Crawler Node
def assign_tasks():
    while not task_queue.empty():
        url = task_queue.get()
        print(f"[Master] Assigned task: Crawl {url}")
        # Here you would normally send this URL to a real Crawler Node over network
        # For simplicity, we'll simulate calling the `crawl_data` method from the crawler.
        crawl_data(url)
        time.sleep(1)  # Simulate some delay
    print("[Master] No more tasks in the queue.")

# Simulate a Crawler Node receiving tasks and returning crawled data
def crawl_data(url):
    print(f"[Crawler] Crawling {url}...")
    # Simulate parsing and extracting content (replace with actual crawler code)
    content = f"Content of {url}"  # Simulated content
    links = [f"{url}/1", f"{url}/2", f"{url}/3"]  # Simulated links

    # Ensure links are added to the task queue for crawling (important!)
    for link in links:
        task_queue.put(link)  # Add extracted links to the task queue

    # Report the crawled data to the Master (through data_queue)
    data_queue.put((url, content, links))
    print(f"[Crawler] Data sent to Master for URL: {url}")

# Simulate basic monitoring of Crawler Nodes
def monitor_crawlers():
    while True:
        print("[Master] Monitoring crawlers... (simulated heartbeat)")
        time.sleep(5)

# Function to forward data to the Indexer
def forward_to_indexer():
    while True:
        if not data_queue.empty():
            url, content, links = data_queue.get()
            print(f"[Master] Sending data to Indexer for URL: {url}")
            # Here you would forward the data to the indexer (e.g., using a shared queue)
            # For simplicity, we'll simulate that the data is being passed to the indexer.
            add_document(url, content)  # This should be the function from the indexer
        time.sleep(1)

if __name__ == "__main__":
    print("[Master] Starting Master Node...")

    load_seed_urls()

    # Start task assignment
    assigner_thread = threading.Thread(target=assign_tasks)
    assigner_thread.start()

    # Start monitoring crawlers
    monitor_thread = threading.Thread(target=monitor_crawlers, daemon=True)
    monitor_thread.start()

    # Start forwarding data to indexer
    forwarder_thread = threading.Thread(target=forward_to_indexer, daemon=True)
    forwarder_thread.start()

    # Wait for assigner thread to finish
    assigner_thread.join()

    # Keep the master running to simulate monitoring
    while True:
        time.sleep(1)
