import re


def get_urls():
    _urls = input("""Please enter seed urls in format like\n
            google.com wikipedia.org etc... \n Input: """)

    _urls = _urls.strip().split(" ")

    _urls = re.split(r'(\.\w{2,63})', _urls)

    seed_urls = []
    for i in range(0, len(urls)-1, 2):
        final_urls.append(urls[i] + urls[i+1])

    for seed in seed_urls:
        if "." not in seed:
            print("Invalid Urls Please retry again!")
            get_urls()
        elif len(seed) < 4:
            print("Invalid Urls Please retry again!")
            get_urls()

    return seed_urls
