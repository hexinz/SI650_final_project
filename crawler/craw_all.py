from craw_single_page import Crawler
import requests
from bs4 import BeautifulSoup
import re
import json

if __name__ == '__main__':
    
    url = 'https://bigbangtrans.wordpress.com/'
    crawler = Crawler()

    # find all links in the page
    sublinks = set()
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a') # get all usable links
    for link in links:
        link = link.get('href')
        if link is not None:
            sublinks.add(link)
    
    # regex = r"https://bigbangtrans.wordpress.com/series-(1)-episode-1-pilot-episode/"

    series_regex = r"series-([0-9]+)"
    episode_regex = r"episode-([0-9]+)"
    title_regex = r"episode-[0-9]+-(.+)/"

    docs = []

    for link in sublinks:
        if 'episode' in link:
            
            series = re.findall(series_regex, link)[0]
            episode = re.findall(episode_regex, link)[0]
            title = re.findall(title_regex, link)[0]

            #try:
            print(link)
            # print(int(series), int(episode), title)
            if title == "the-lizard-spock-expansion":
                series = 2
            transcript_dict = crawler.craw_page_wordpress(link, int(series), int(episode), title)

            AllLines = transcript_dict['AllLines']
            for line_idx, (actor, line) in enumerate(AllLines):
                doc = {
                    "line": line,
                    "actor": actor,
                    "line_idx": line_idx,
                    'series': int(series),
                    'episode': int(episode),
                    'title': ' '.join(title.split('-')),
                }
                docs.append(json.dumps(doc))

    with open("documents.jsonl", 'w+') as fout:
        for docid, doc in enumerate(docs):
            fout.write(json.dumps({"id": str(docid), "contents": doc})+"\n")
