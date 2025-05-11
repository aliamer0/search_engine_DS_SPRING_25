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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - Crawler - %(levelname)s - %(message)s')

def crawler_process():

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    crawler_nodes = size // 2
    cursor = conn.cursor(buffered = True)
    robot_parsers = {}
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"

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
            
            try:
                parsed_url = urlparse(url_to_crawl)
                base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

                # Load and cache robots.txt for this domain
                if base_url not in robot_parsers:
                    rp = robotparser.RobotFileParser()
                    robots_url = urljoin(base_url, "/robots.txt")
                    try:
                        rp.set_url(robots_url)
                        rp.read()
                        robot_parsers[base_url] = rp
                    except Exception as e:
                        logging.warning(f"Crawler {rank} failed to fetch robots.txt for {base_url}: {str(e)}")
                        # fallback: if robots.txt not available, allow crawling
                        rp = robotparser.RobotFileParser()
                        rp.parse(["User-agent: *", "Disallow:"])
                        robot_parsers[base_url] = rp

                if not robot_parsers[base_url].can_fetch(user_agent, url_to_crawl):
                    logging.info(f"Crawler {rank}: Disallowed by robots.txt: {url_to_crawl}")
                    comm.send(rank, dest=0, tag=99)
                    continue

                headers = {'User-Agent': user_agent}
                try:
                    response = requests.get(url_to_crawl, headers=headers, timeout=4)
                    response.raise_for_status()

                except requests.exceptions.Timeout as e:
                    logging.warning(f"Crawler {rank}: Timeout while fetching {url_to_crawl}: {e}")
                    comm.send((rank,url_to_crawl), dest=0, tag=9)
                    continue
                
                except requests.exceptions.RequestException as e:
                    error_message = f"{type(e).__name__}: {str(e)}"
                    logging.warning(f"Crawler {rank}: Failed to fetch {url_to_crawl} due to {type(e).__name__}: {e}")
                    comm.send((url_to_crawl, error_message, rank), dest=0, tag=999)
                    continue

                
                
                if response.status_code == 200:
                    html = response.text
                else:
                    error_message = f"{type(e).__name__}: {str(e)}"
                    logging.info(f"Crawler {rank} Failed to crawl: {url_to_crawl} ... Status: {response.status_code}")
                    comm.send((url_to_crawl, error_message, rank), dest=0, tag=999)
                    continue


                soup = BeautifulSoup(html, "html.parser")
                links = []
                for a_tag in soup.find_all("a", href=True):
                    href = a_tag["href"]
                    parsed_href = urlparse(href)
                    if href.startswith("//"):
                        absolute_url = f"{parsed_url.scheme}:{href}"
                        links.append(absolute_url)
                    elif parsed_href.netloc == "":  # it's a relative URL
                        absolute_url = urljoin(url_to_crawl, href)
                        links.append(absolute_url)
                    else:  # it's an absolute URL
                        links.append(href)

                html_text = soup.get_text(separator="\n")

                sql = "INSERT INTO crawled_pages (URL, html, links, retrieved) VALUES (%s, %s, %s, %s)"
                values = (url_to_crawl, html, json.dumps(links), False)
                cursor.execute(sql, values)
                conn.commit()
                
                extracted_urls = links
                logging.info(f"Crawler {rank} crawled {url_to_crawl}, extracted {len(extracted_urls)} URLS.")
                comm.send(extracted_urls, dest=0, tag = 1)

                # send content to the indexer available
                indexers = comm.recv(source= 0 , tag=3)
                if indexers:
                    indexer = indexers.pop()
                    comm.send((url_to_crawl, html_text), dest = indexer, tag = 2)

                comm.send(rank, dest = 0, tag = 99)


            except Exception as e:
                error_message = f"{type(e).__name__}: {str(e)}"
                logging.error(f"crawler {rank} error crawling {url_to_crawl}: {str(e)}")
                comm.send((url_to_crawl, error_message, rank), dest=0, tag=999)

        cursor.close()
