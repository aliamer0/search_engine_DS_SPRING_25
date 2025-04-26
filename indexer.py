from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import os

# Step 1: Define the index schema
schema = Schema(url=ID(stored=True, unique=True), content=TEXT)

# Step 2: Create or open the index directory
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
    idx = index.create_in("indexdir", schema)
else:
    idx = index.open_dir("indexdir")


# Step 3: Function to add a new document to the index
def add_document(url, content):
    writer = idx.writer()
    writer.add_document(url=url, content=content)
    writer.commit()
    print(f"[Indexer] Document added for URL: {url}")


# Step 4: Function to search for a keyword
def search_keyword(keyword):
    with idx.searcher() as searcher:
        query = QueryParser("content", idx.schema).parse(keyword)
        results = searcher.search(query)
        print(f"[Search Results for '{keyword}']:")
        for result in results:
            print(f"- {result['url']}")


# Step 5: Simulate receiving data from Crawler Node
if __name__ == "__main__":
    # Example: Simulated "ingestion" of crawled data
    example_url = "https://en.wikipedia.org/wiki/SS_Normandie"
    example_content = open("gfg-wiki.html", encoding="utf-8").read()

    # In real project: you would receive URL + Text from Crawler over queue or direct call

    add_document(example_url, example_content)

    # Now you can search
    search_keyword("luxury")
    search_keyword("France")
