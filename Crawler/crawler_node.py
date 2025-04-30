from mpi4py import MPI
import time
import logging



def crawler_process():

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    crawler_nodes = size // 2
    if ((rank != 0) and (size <= crawler_nodes)):
        logging.info(f"Crawler node started with rank {rank} of {size}")

        while True:

            status = MPI.Status()
            url_to_crawl = comm.recv(source=0, tag=0, status=status)
            if not url_to_crawl:
                logging.info(f"Crawler {rank} received shutdown signal. Exiting.")
                break

            try:
                # Web crawling logic
                time.sleep(2)
                extracted_urls = [f"http://example.com/page_from_crawler_{rank}_{i}" for i in range(2)]

                logging.info(f"Crawler {rank} crawled {url_to_crawl}, extracted {len(extracted_urls)} URLS.")
                comm.send(extracted_urls, dest=0, tag = 1)

                # send content for the indexer



            except Exception as e:
                logging.error(f"crawler {rank} error crawling {url_to_crawl}: ")
                comm.send(f"Error crawling {url_to_crawl}: {e}", dest=0, tag=999)

if __name__ == "__main__":
    crawler_process()
