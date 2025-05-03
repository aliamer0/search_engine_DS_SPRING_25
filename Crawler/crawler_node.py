from mpi4py import MPI
import time
import logging
from Assets.db import conn
import json
import ast
import traceback
import requests
from urllib.parse import urljoin, urlparse
import urllib.robotparser as robotparser
import json
from bs4 import BeautifulSoup

def crawler_process():

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    crawler_nodes = size // 2
    cursor = conn.cursor()

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
                response = requests.get(url_to_crawl)
                if response.status_code == 200:
                    html = response.text
                else:
                    logging.info("Crawler {rank} Failed to crawl: {url_to_crawl} ... Skipping.")
                    comm.send(rank, dest=0, tag=99)
                    continue

                soup = BeautifulSoup(html, "html.parser")
                links = []
                for a_tag in soup.find_all("a", href=True):
                    absolute_url = urljoin(url_to_crawl, a_tag["href"])
                    links.append(absolute_url)

                sql = "INSERT INTO crawled_pages (URL, html, links, retrieved) VALUES (%s, %s, %s, %s)"
                values = (url_to_crawl, html, json.dumps(links), False)
                cursor.execute(sql, values)
                conn.commit()
                
                extracted_urls = links
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

