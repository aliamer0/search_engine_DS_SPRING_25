from mpi4py import MPI
import time
import logging
from UI.ui import get_urls
import redis
from Crawler.crawler_node import crawler_process
from Indexer.indexer_node import indexer_process
from Assets.db import conn
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - Master - %(levelname)s - %(message)s')

def master_process():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    status = MPI.Status()
    cursor = conn.cursor()

    if (rank == 0):
        logging.info(f"Master node started with {rank} of {size}")

        # Initialization of task queue
        #app.start()
        # Implementation of database connection

        r = redis.StrictRedis(host = "localhost", port=6379, db = 0)
        r_results = redis.StrictRedis(host = "localhost", port=6379, db = 1)
        r.select(0)  # Explicitly select the correct DB


        # dividing the size through crawerls, indexers, and master
        crawler_nodes = size // 2
        indexer_nodes = size - crawler_nodes

        total_nodes = indexer_nodes + crawler_nodes
        if total_nodes == size:
            indexer_nodes -= 1

        if crawler_nodes <= 0 or indexer_nodes <= 0:
            logging.error("""Not enough nodes to run crawler and indexer.
            Need at least 3 nodes (1 master, 1 crawler, 1 indexer)""")
            return

        active_crawler_nodes = set(range(1, 1 + crawler_nodes)) # Ranks for crawler nodes (assuming rank 0 is master)
        active_indexer_nodes = set(range(1 + crawler_nodes, size)) # Ranks for indexer nodes

        logging.info(f"Active Crawler Nodes: {active_crawler_nodes}")
        logging.info(f"Active Indexer Nodes: {active_indexer_nodes}")

        seed_urls = sys.argv[1] if len(sys.argv) > 1 else ""
        seed_urls = seed_urls.split(',')

        task_count = 0
        crawler_tasks_assigned = 0

        print("seed urls:", seed_urls)
        for url in seed_urls:
            try:
                r.rpush('urls', url.encode('utf-8'))
            except Exception as e:
                logging.error(f"Redis direct push failed: {str(e)}")

        while (r.llen('urls') > 0) or (crawler_tasks_assigned > 0):
            if crawler_tasks_assigned > 0:
                if comm.iprobe(source = MPI.ANY_SOURCE, tag = MPI.ANY_TAG, status = status):
                    message_source = status.Get_source()
                    message_tag = status.Get_tag()
                    message_data = comm.recv(source=message_source, tag=message_tag)

                    if message_tag == 1:
                        crawler_tasks_assigned -= 1
                        new_urls = message_data
                        
                        if new_urls:
                            for url in new_urls:
                                try:
                                    r.rpush('urls', url.encode('utf-8'))
                                except Exception as e:
                                    logging.error(f"Redis direct push failed: {str(e)}")
                                
                            logging.info(f"""Master received URLs from Crawler {message_source},
                            URLs added to queue: {len(new_urls)},
                            URLs in the queue: {r.llen('urls')},
                            Tasks assigned: {crawler_tasks_assigned}""")

                    #timeouts of crawler
                    elif message_tag == 9:
                        rank, url = message_data
                        logging.info(f"Crawler {rank} timedout reassigning ...")
                        try:
                            r.rpush('urls', url.encode('utf-8'))
                        except Exception as e:
                            logging.error(f"Redis direct push failed: {str(e)}")
                        active_crawler_nodes.add(rank)                        

                    elif message_tag == 99:
                        if message_data in range(1, crawler_nodes+1):
                            logging.info(f"""Crawler {message_source},
                            status: Available""")
                            active_crawler_nodes.add(message_data)
                        if message_data in range(crawler_nodes+1, size):
                            logging.info(f"""Indexer {message_source},
                            status: Available""")
                            active_indexer_nodes.add(message_data)


                    elif message_tag == 999:
                        if message_source in range(1, crawler_nodes+1):
                            url, error, rank = message_data
                            logging.error(f"""Crawler {message_source}
                            reported error: {error}""")
                            try:
                                r.rpush('urls', url.encode('utf-8'))
                            except Exception as e:
                                logging.error(f"Redis direct push failed: {str(e)}")
                            active_crawler_nodes.add(rank)


                        elif message_source in (crawler_nodes+1, size):
                            rank, error = message_data
                            logging.error(f"""Indexer {message_source}
                            reported error: error""")
                            active_indexer_nodes.add(rank)


                            
                        crawler_tasks_assigned -= 1

            while (r.llen('urls') > 0) and active_crawler_nodes:

                url_to_crawl = r.lpop("urls")
                url_to_crawl = url_to_crawl.decode("utf-8")
                
                available_crawler_rank = active_crawler_nodes.pop()
                
                task_id = task_count
                task_count += 1
                logging.info(f"Master sending URL {url_to_crawl} to Crawler {available_crawler_rank}")
                comm.send(url_to_crawl, dest = available_crawler_rank, tag = 0)
                comm.send(active_indexer_nodes, dest = available_crawler_rank, tag = 3)
                crawler_tasks_assigned += 1
                logging.info(f"""Master assigned task {task_id} (crawl {url_to_crawl})
                to Crawler {available_crawler_rank}, Tasks assigned: {crawler_tasks_assigned}""")

        logging.info("""Master node finished URL distribution. Waiting for crawlers to complete...""")
        for crawler_rank in active_crawler_nodes:
            comm.send(None, dest=crawler_rank, tag=0)
        cursor.execute("DELETE FROM crawled_pages")
        conn.commit()
        logging.info(""" Cache data erased """)
        cursor.close()
        conn.close()


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    if rank == 0:
        master_process()
    elif rank != 0 and rank <= (size//2):
        crawler_process()
    else:
        indexer_process()
