from mpi4py import MPI
import time
import logging
from Assets.db import conn
import Indexer.whoosh_indexer

logging.basicConfig(level = logging.INFO, format= "%(asctime)s - Indexer - %(levelname)s - %(message)s")

def indexer_process():

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    cursor = conn.cursor(buffered=True)

    if (rank > (size//2)):
        logging.info(f"Indexer node started with rank {rank} of {size}")

        # initialize
        comm.send(rank, dest=0, tag=99)

        while True:
            status = MPI.Status()
            try:
                url, content_to_index = comm.recv(source=MPI.ANY_SOURCE, tag=2, status=status)
            except MPI.Exception as e:
                if e.Get_error_class() == MPI.ERR_PROC_FAILED:
                    comm = comm.Shrink()
                    
            source_rank = status.Get_source()
            if content_to_index:
                sql = "SELECT retrieved FROM crawled_pages WHERE url = %s"
                cursor.execute(sql, (url,))
                result = cursor.fetchone()
                if result:
                    retrieved, = result
                    if retrieved == True:
                        try:
                            comm.send(rank, dest=0, tag=99)
                        except MPI.Exception as e:
                            if e.Get_error_class() == MPI.ERR_PROC_FAILED:
                                comm = comm.Shrink()
                        
                        continue
                else:
                    cursor.fetchall()

            if content_to_index is None:
                logging.info(f"Indexer {rank} received shutdown signal. Exiting")
                break

            logging.info(f"indexer {rank} received content from Crawler {source_rank} to index")

            try:

                #indexing
                Indexer.whoosh_indexer.add_document(url, content_to_index)

                logging.info(f"Indexer {rank} indexed content from Crawler {source_rank}.")

                try:
                    comm.send(rank, dest = 0, tag = 99)
                except MPI.Exception as e:
                    if e.Get_error_class() == MPI.ERR_PROC_FAILED:
                        comm = comm.Shrink()

                cursor.execute("UPDATE crawled_pages SET retrieved = TRUE WHERE url = %s", (url,))
                conn.commit()


            except Exception as e:
                error_message = f"{type(e).__name__}: {str(e)}"
                logging.error(f"Indexer {rank} error indexing content from Crawler {source_rank}: {e}")
                try:
                    comm.send((rank, error_message), dest=0, tag=999)
                except MPI.Exception as e:
                    if e.Get_error_class() == MPI.ERR_PROC_FAILED:
                        comm = comm.Shrink()
                    
        cursor.close()
