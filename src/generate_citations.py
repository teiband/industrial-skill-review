#!/usr/bin/env python3.6
import os
import traceback

import pandas as pd
import requests
from bs4 import BeautifulSoup
from scholarly import scholarly, ProxyGenerator

# nltk.download('wordnet')

USE_PROXY = True

if USE_PROXY:
    print("getting proxy generator...")
    pg = ProxyGenerator()
    print("getting free proxy...")
    success = pg.FreeProxies(timeout=10, wait_time=120)
    print(f"using free proxy: {success}")
    scholarly.use_proxy(pg)

# author = next(scholarly.search_author('Steven A Cholewiak'))
# scholarly.pprint(author)

this_file_dir = os.path.dirname(os.path.realpath(__file__))
resultsFile = os.path.join(this_file_dir, "../data/in/20220127_skillTaxonomy.csv")

taxonomy = pd.read_csv(resultsFile, delimiter=';')
# taxonomy = taxonomy.loc[taxonomy['relevant'] == 'Y']

taxonomyExp = pd.DataFrame(columns=['author', 'link', 'relevant', 'how', 'requirements', 'ind', 'hier',
                                    'similarity', 'skillclass', 'identified skillclass', 'skill',
                                    'identified skill', 'primitive', 'identified primitive',
                                    'parametrizedskill', 'identified parametrizedskill', 'task',
                                    'identified task', 'request', 'identified request', 'process',
                                    'identified process', 'arch', 'impl', 'param', 'paramtype'])

bibtex_str = ""


def get_webpage_title_by_url(url: str) -> str:
    # making requests instance

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/39.0.2171.95 Safari/537.36'}

    reqs = requests.get(url, headers=headers)

    # using the BeaitifulSoup module
    soup = BeautifulSoup(reqs.text, 'html.parser')

    # displaying the title
    title = soup.title.string
    return title


# clear file
out_file_name = os.path.join(this_file_dir, "..", "data/out/" + "bibtex.bib")
with open(out_file_name, 'w') as outfile:
    pass

print("looping over references from table...")
for i, e in taxonomy.iterrows():
    if not e['link'].startswith("http"):
        continue
    try:

        title = get_webpage_title_by_url(e['link'])
        search_string = title
        # search_string = " ".join([str(f) for f in e])
        print(f"Searching for: {search_string}")
        pub = scholarly.search_single_pub(search_string)
        scholarly.pprint(pub)
        print("getting bibtex entry...")
        bibtex_entry = scholarly.bibtex(pub)
        bibtex_str += bibtex_entry
        with open(out_file_name, 'a') as outfile:
            outfile.write(bibtex_entry + "\n\n")
    except:
        traceback.print_exc()
