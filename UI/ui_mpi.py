from mpi4py import MPI
from whoosh import index
from whoosh.qparser import QueryParser, OrGroup

import sys
import os

def search_local_index(keyword, index_dir):
    if not index.exists_in(index_dir):
        return []

    idx = index.open_dir(index_dir)
    with idx.searcher() as searcher:
        parser = QueryParser("content", idx.schema, group=OrGroup.factory(0.9))
        query = parser.parse(keyword)
        results = searcher.search(query)
        return [r['url'] for r in results]

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    index_dir = sys.argv[2]  # each node gets its local indexdir as argument

    if rank == 0:
        keyword = sys.argv[1]

        # Broadcast query to all ranks
        for dest in range(1, size):
            comm.send(keyword, dest=dest, tag=11)

        # Collect results
        all_results = []
        for source in range(1, size):
            urls = comm.recv(source=source, tag=22)
            all_results.extend(urls)

        # Display aggregated results
        print("\nAggregated Results:")
        for url in all_results:
            print(url)

    else:
        # Worker node: receive query
        keyword = comm.recv(source=0, tag=11)
        urls = search_local_index(keyword, index_dir)
        comm.send(urls, dest=0, tag=22)

if __name__ == "__main__":
    main()
