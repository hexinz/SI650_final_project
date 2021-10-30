import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json
import os
import re

url = 'https://bigbangtheory.fandom.com/wiki/Transcripts/'

def clean_me(html):
    soup = BeautifulSoup(html)
    for s in soup(['script', 'style']):
        s.decompose()
    return ' '.join(soup.stripped_strings)

class Crawler():
    
    def __init__(self):
        pass
        # self.base_url = base_url

    def craw_page(self, url, season, title):

        # page_name = os.path.basename(url)
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')

        regex = r"-_Episode_([0-9]{1,2})_-"
        episode = 6#int(re.findall(regex, html)[0])

        transcript_dict = {
            'Season': 1,
            'Episode': episode,
            'Title': title,
            'Actor2Line': dict(list()),
            'Actor2Profile': dict(),
            'AllLines': list()
        }

        br = soup.find_all('tbody')
        transcript = br[0]

        transcript_data = transcript.find_all('tr')

        line_idx = 0
        for pair in transcript_data[1:]:
            
            actor, content = pair.find_all('td')

            # get content
            if content.string is None:
                if len(content.find_all('i')) > 0:
                    try:
                        actor_line = content.i.string.rstrip()
                    except AttributeError:
                        try:
                            actor_line = content.a.string + content.i.contents[1]
                        except TypeError:
                            actor_line = "" 
                            # print(content.find_all('i')[0].contents)
                            for item in content.find_all('i')[0].contents:
                                if item.string is not None:
                                    actor_line += item.string.rstrip()
                                if isinstance(item, str):
                                    actor_line += item
                else:
                    continue
            else:
                actor_line = content.string.rstrip()

            # get actor
            if len(actor.find_all('a')) > 0:
                actor_name = actor.a.string.rstrip()
                actor_link = str(actor.a.get('href'))
                transcript_dict['Actor2Profile'][actor_name] = actor_link
            else:
                if actor.string is not None:
                    actor_name = actor.string.rstrip()
                    if actor_name == "":
                        actor_name = "Scene"
                else:
                    actor_name = "Scene"

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

        save_path = os.path.join('transcripts', 'season'+str(season), title+'.json')
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'w+') as fout:
            json.dump(transcript_dict, fout, indent=4)

if __name__ == '__main__':
    crawler = Crawler()
    crawler.craw_page(url+'The Cooper-Nowitzki Theorem', 2, 'The Cooper-Nowitzki Theorem')