#!/usr/bin/env python3.6
import os
import time
import traceback

import pandas as pd
import requests
from bs4 import BeautifulSoup
from scholarly import scholarly, ProxyGenerator

# nltk.download('wordnet')

# from: https://free-proxy-list.net/
# success = pg.SingleProxy(https="45.79.230.234")

PROXY_MODE = 'multi'  # 'fixed' # 'none', 'multi' # only working method is 'multi' while DLR ssh connection was open
FIXED_PROXY = "127.0.0.1:8080"  # supports google and https
# FIXED_PROXY = "45.79.230.234" # supports google and https
bibtex_file_name = input("Enter output bib file name:\n")

start_at_row = input("Enter start row of table:\n")

if PROXY_MODE == 'fixed':
    print(f"I will use a fixed proxy: {FIXED_PROXY}")
    print("setup proxy generator...")
    pg = ProxyGenerator()
    pg.SingleProxy(https=FIXED_PROXY)
    scholarly.use_proxy(pg)
elif PROXY_MODE == 'multi':
    print("I will use multiple proxies")
    print("setup proxy generator...")
    pg = ProxyGenerator()
    print("obtain free proxies...")
    pg.FreeProxies()
    scholarly.use_proxy(pg)
elif PROXY_MODE == 'none':
    print("I will not use any proxy")


def set_new_proxy():
    if PROXY_MODE == 'multi':
        try:
            print("getting next proxy...")
            pg.get_next_proxy()
            print("setting new proxy...", end='')
            scholarly.use_proxy(pg)
            print("done!")
        except:
            print("creating new proxy list...")
            time.sleep(10.0)
            pg = ProxyGenerator()
            pg.FreeProxies()
            scholarly.use_proxy(pg)


set_new_proxy()

# author = next(scholarly.search_author('Steven A Cholewiak'))
# scholarly.pprint(author)

this_file_dir = os.path.dirname(os.path.realpath(__file__))
resultsFile = os.path.join(this_file_dir, "../data/in/20220202_skillTaxonomy.csv")

taxonomy = pd.read_csv(resultsFile, delimiter=';')
# taxonomy = taxonomy.loc[taxonomy['relevant'] == 'Y']

taxonomy = taxonomy[int(start_at_row) - 1:]

bibtex_str = ""


def get_webpage_title_by_url(url: str) -> str:
    # making requests instance

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/39.0.2171.95 Safari/537.36'}

    reqs = requests.get(url, headers=headers)

    # using the BeaitifulSoup module
    soup = BeautifulSoup(reqs.text, 'html.parser')

    try:
        title = soup.title.string
    except:
        title = None
    return title


# clear file content
out_file_name = os.path.join(this_file_dir, "..", "data/out/" + bibtex_file_name)
with open(out_file_name, 'w') as outfile:
    pass

# create finished_authors file if not existing
finished_authors_file_name = os.path.join(this_file_dir, "..", "data/out/" + "finished_authors_bibtex.txt")
# with open(finished_authors_file_name, 'a') as outfile:
#    pass


# create failed_authors file if not existing
failed_authors_file_name = os.path.join(this_file_dir, "..", "data/out/" + "failed_authors_bibtex.txt")
with open(failed_authors_file_name, 'w') as outfile:
    pass

print("looping over references from table...")
for i, e in taxonomy.iterrows():
    author = e['author']
    if not e['link'].startswith("http"):
        continue
    # if author in finished_authors:
    #    continue
    print(f"current entry: {author}")
    print("-------------------------------------------------")
    print("getting webpage title...")
    title = get_webpage_title_by_url(e['link'])
    if not title:
        print("Could not extract title from webpage, maybe due to to 'http' and not 'https' adress.")
        print("writing the failed author to file...", end='')
        with open(failed_authors_file_name, 'a') as outfile:
            outfile.write(author + "\n")
        print("done")
        continue

    # get publication data
    while True:
        try:
            search_string = title
            # search_string = " ".join([str(f) for f in e])
            print(f"searching: {search_string}")
            pub = scholarly.search_single_pub(search_string)
            scholarly.pprint(pub)
            break
        except:
            traceback.print_exc()
            print("ERROR: trying now again with another proxy")
            set_new_proxy()
    # get bibtex data
    time.sleep(2.0)
    while True:
        try:
            print("getting bibtex entry...")
            bibtex_entry = scholarly.bibtex(pub)
            bibtex_str += bibtex_entry
            print("writing to file...")
            with open(out_file_name, 'a') as outfile:
                outfile.write(bibtex_entry)
            break
        except:
            traceback.print_exc()
            print("ERROR: trying now again with another proxy")
            set_new_proxy()
