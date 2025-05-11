import argparse
from Indexer import whoosh_indexer

def main():
    parser = argparse.ArgumentParser(description="Whoosh Indexer CLI")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search the index for a keyword")
    search_parser.add_argument("keyword", type=str, help="Keyword to search in the index")

    args = parser.parse_args()

    if args.command == "search":
        results = whoosh_indexer.search_keyword(args.keyword)
        if results:
            print(f"\nFound {len(results)} result(s):")
            for url in results:
                print(f"- {url}")
        else:
            print("No results found.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

