from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer
import os, shutil

def get_or_create_index():
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
        schema = Schema(url=ID(stored=True, unique=True), content=TEXT(analyzer=StemmingAnalyzer()))
        return index.create_in("indexdir", schema)
    else:
        return index.open_dir("indexdir")

def add_document(url, content):
    idx = get_or_create_index()
    writer = idx.writer()
    writer.add_document(url=url, content=content)
    writer.commit()

def search_keyword(keyword):
    idx = get_or_create_index()
    with idx.searcher() as searcher:
        from whoosh.qparser import QueryParser, OrGroup
        parser = QueryParser("content", idx.schema, group=OrGroup.factory(0.9))
        query = parser.parse(keyword)
        results = searcher.search(query)
        return [r['url'] for r in results]
