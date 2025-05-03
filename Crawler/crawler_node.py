from mpi4py import MPI
import time
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Crawler.spiders.distributed_spider import DistributedSpider
from Assets.db import conn, cursor
import json
import ast
import traceback
import threading



def crawler_process():

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    crawler_nodes = size // 2


    MPI_TIMEOUT = 10
    
    if ((rank != 0) and (rank <= crawler_nodes)):
        logging.info(f"Crawler node started with rank {rank} of {size}")

        comm.send(rank, dest=0, tag=99)


        while True:
            status = MPI.Status()
            url_to_crawl = comm.recv(source=0, tag=0, status=status)
            sql = "SELECT links, html FROM crawled_pages WHERE url= %s"
            cursor.execute(sql, (url_to_crawl, ))
            result = cursor.fetchone()

            if result:
                comm.send(rank, dest=0, tag=99)
                continue


            if not url_to_crawl:
                logging.info(f"Crawler {rank} received shutdown signal. Exiting.")    
                break
            
            start_time = time.time()
            try:
                process = CrawlerProcess(get_project_settings())
                process.crawl(DistributedSpider, start_url = url_to_crawl)
                process.start()
                process.stop()
                thread = threading.Thread(target=worker)
                cursor.execute(sql, (url_to_crawl, ))
                result = cursor.fetchone()
                if result:
                    links, html = result

                
                extracted_urls = ast.literal_eval(links) if links else []
                logging.info(f"Crawler {rank} crawled {url_to_crawl}, extracted {len(extracted_urls)} URLS.")
                comm.send(extracted_urls, dest=0, tag = 1)

                # send content to the indexer available
                comm.send(rank, dest = 0, tag = 99)
                indexers = comm.recv(source= 0 , tag=3)
                if indexers:
                    indexer = indexers.pop()
                    comm.send((url_to_crawl,html), dest = indexer, tag = 2)



            except Exception as e:
                error_message = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
                logging.error(f"crawler {rank} error crawling {url_to_crawl}: {str(e)}")
                comm.send((url_to_crawl, error_message, rank), dest=0, tag=999)
 


