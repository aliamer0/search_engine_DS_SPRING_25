import re


def get_urls():
    urls = input("""Please enter seed urls in format like\n
            google.com wikipedia.org etc... \n Input: """)

    urls = urls.strip().split(" ")
    
    return urls

