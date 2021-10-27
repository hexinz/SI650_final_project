from craw_single_page import Crawler
import requests
from bs4 import BeautifulSoup
season=1

url = 'https://bigbangtheory.fandom.com/wiki/Season_1'

titles = ['']

crawler = Crawler()


if __name__ == '__main__':
    
    sublinks = set()

    r = requests.get(url)
    r.encoding = r.apparent_encoding
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    td = soup.find_all('td')
    for dummy in td:
        links = dummy.find_all('a')
        for link in links:
            link = link.get('href')
            if link is not None:
                sublinks.add(link)
    
    for i, link in enumerate(sublinks):
        if link.startswith('/wiki/'):
            subname = link[6:].rstrip()
            print(subname)

            try:
                url = 'https://bigbangtheory.fandom.com/wiki/Transcripts/'+subname
                crawler.craw_page(url, season, i, subname)

            except Exception as e:
                print(e)

