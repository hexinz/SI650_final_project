import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json

url = 'https://bigbangtheory.fandom.com/wiki/Transcripts/Pilot'

class Crawler():
    
    def __init__(self):
        pass
        # self.base_url = base_url

    def craw_page(self, url, season, episode, title):

        # page_name = os.path.basename(url)

        transcript_dict = {
            'Season': 1,
            'Episode': episode,
            'Title': title,
            'Actor2Line': dict(list()),
            'Actor2Profile': dict(),
            'AllLines': list()
        }

        r = requests.get(url)
        r.encoding = r.apparent_encoding
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')

        br = soup.find_all('tbody')
        transcript = br[0]

        transcript_data = transcript.find_all('tr')

        line_idx = 0
        for pair in transcript_data[1:]:
            
            actor, content = pair.find_all('td')
            if content.string is None:
                continue

            if len(actor.find_all('a')) > 0:
                actor_name = actor.a.string.rstrip()
                actor_link = str(actor.a.get('href'))
                transcript_dict['Actor2Profile'][actor_name] = actor_link
            else:
                actor_name = actor.string.rstrip()
                
            actor_line = content.string.rstrip()
            
            assert isinstance(actor_name, str)
            assert isinstance(actor_line, str)
            
            if actor_name not in transcript_dict['Actor2Line']:
                transcript_dict['Actor2Line'][actor_name] = [(line_idx, actor_line)]
            else:
                transcript_dict['Actor2Line'][actor_name].append((line_idx, actor_line))
            transcript_dict['AllLines'].append(actor_line)
            line_idx += 1
                
            #except Exception as e:
            #    print("Failed processing at idx "+str(line_idx))
            #    print(e)
        # print(transcript_dict)

        with open('transcripts/'+title+'.json', 'w+') as fout:
            json.dump(transcript_dict, fout, indent=4)