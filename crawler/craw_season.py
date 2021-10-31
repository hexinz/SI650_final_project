from craw_single_page import Crawler
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    
    for season in range(1,3):

        url = 'https://bigbangtheory.fandom.com/wiki/Season_'+str(season)
        crawler = Crawler()

        sublinks = set()

        r = requests.get(url)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        td = soup.find_all('td')

        for dummy in td:
            links = dummy.find_all('a') # get all usable links
            for link in links:
                link = link.get('href')
                if link is not None:
                    sublinks.add(link)
        
        for link in sublinks:
            if link.startswith('/wiki/'):
                subname = link[6:].rstrip()
                print(subname)

                try:
                    url = 'https://bigbangtheory.fandom.com/wiki/Transcripts/'+subname
                    crawler.craw_page_fandom(url, season, subname)

                except Exception as e:
                    print(e)

