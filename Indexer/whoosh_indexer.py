import os
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer
import shutil

# Create index dir if it doesn't exist
def setup_index():
    schema = Schema(url=ID(stored=True, unique=True), content=TEXT(analyzer=StemmingAnalyzer()))
    if os.path.exists("indexdir"):
        shutil.rmtree("indexdir")
    os.mkdir("indexdir")
    return index.create_in("indexdir", schema)


def add_document(url, content):
    writer = idx.writer()
    writer.add_document(url=url, content=content)
    writer.commit()

def search_keyword(keyword):
    from whoosh.qparser import QueryParser, OrGroup
    with idx.searcher() as searcher:
        parser = QueryParser("content", idx.schema, group=OrGroup.factory(0.9))
        query = parser.parse(keyword)
        results = searcher.search(query)
        return [r['url'] for r in results]
