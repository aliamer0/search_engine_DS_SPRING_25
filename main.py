from multiprocessing import Process, Queue
from parser import crawl_page
from indexer import add_document, search_keyword


def crawler_process(queue, seed_url="https://en.wikipedia.org/wiki/SS_Normandie"): # use a default URL
    crawled_urls = set()
    to_crawl = [seed_url]  # Start with a seed URL

    while to_crawl:
        url = to_crawl.pop()
        if not url:  # Skip empty URLs
            continue
        if url in crawled_urls:
            continue  # Skip if URL has already been crawled
        crawled_urls.add(url)

        print(f"[Crawler] Crawling {url}...")
        response = crawl_page(url)
        if response:
            url, text, links = response
            queue.put((url, text))  # Send data to the indexer
            to_crawl.extend(links)  # Add new links to the crawling queue
        else:
            print(f"[Crawler] Failed to crawl {url}")


def indexer_process(queue, max_urls=10):
    processed_count = 0
    while processed_count < max_urls:
        if not queue.empty():
            url, text = queue.get()
            print(f"[Indexer] Adding document for {url}")
            add_document(url, text)
            #search_keyword("ship")
            #search_keyword("UK")
            processed_count += 1
    print("[Indexer] Finished processing the required number of URLs.")


if __name__ == "__main__":
    q = Queue()

    # Create processes
    p1 = Process(target=crawler_process, args=(q,))
    p2 = Process(target=indexer_process, args=(q,))

    # Start processes
    p1.start()
    p2.start()

    # Join processes
    p1.join()  # Wait for crawler process to finish
    p2.join()  # Wait for indexer process to finish (this can run indefinitely if you want it to)
