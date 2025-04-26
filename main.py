from multiprocessing import Process, Queue
from parser import crawl_page
from indexer import add_document, search_keyword

def crawler_process(queue):
    url = "https://en.wikipedia.org/wiki/SS_Normandie"
    # crawl the page
    response = crawl_page(url)
    if response:
        url, text, links = response
        queue.put((url, text))  # Send it to indexer

def indexer_process(queue):
    while True:
        if not queue.empty():
            url, text = queue.get()
            add_document(url, text)
            # Optional: after indexing, you could immediately search
            search_keyword("ship")
            search_keyword("UK")

if __name__ == "__main__":
    q = Queue()

    # Create processes
    p1 = Process(target=crawler_process, args=(q,))
    p2 = Process(target=indexer_process, args=(q,))

    # Start processes
    p1.start()
    p2.start()

    # Join processes
    p1.join()
    # p2 keeps running to process future data (you can terminate manually)
