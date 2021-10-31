import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json
import os
import re

url = 'https://bigbangtheory.fandom.com/wiki/Transcripts/'

class Crawler():
    
    def __init__(self):
        pass
        # self.base_url = base_url

    def matching(self, content):

        actor_line_regex = r"^(.+)[:;][ ]?(.+)"

        match = re.findall(actor_line_regex, content)
                
        if len(match) == 1: # found perfect match
            actor, line = match[0]
        elif len(match) == 0: # no match found
            actor = "Scene"
            line = content.strip()
        else:
            print("ERROR!")
            exit(1)
        
        return actor, line

    def craw_page_wordpress(self, url, season, episode, title, save_file=True):
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')

        transcript_dict = {
            'Season': season,
            'Episode': episode,
            'Title': ' '.join(title.split('-')),
            'Actor2Line': dict(list()),
            'AllLines': list(),
            'url': url,
        }

        cleaned = []

        for p in soup.find_all('p'):

            if p.em is not None: # remove any useless em tags
                str_p = str(p)
                str_p = str_p.replace("<em>", "")
                str_p = str_p.replace("</em>", "")
                p = BeautifulSoup(str_p, 'html.parser')

            if p.i is not None: # remove any useless i tags
                str_p = str(p)
                str_p = str_p.replace("<i>", "")
                str_p = str_p.replace("</i>", "")
                p = BeautifulSoup(str_p, 'html.parser')

            if p.string is not None: # directly extractable

                cleaned.append(p.string)

            elif p.span is not None: # most annoying case, use .text attribute to get 

                for content in p.span.text.strip().split('\n'):

                    if content.strip() == "":
                        continue

                    cleaned.append(content)

            else: # no string or em
                print("WARNING: Give up ", p)
                continue

        for line_idx, content in enumerate(cleaned):
            
            actor, line = self.matching(content)

            if actor == "Scene":
                if line.strip() != "":
                    if line == ':': # remove redundancy
                        continue
                    print(f"* scene[ {line} ]")
                else:
                    continue

            if actor not in transcript_dict['Actor2Line']:
                transcript_dict['Actor2Line'][actor] = [(line_idx, line)]
            else:
                transcript_dict['Actor2Line'][actor].append((line_idx, line))

            transcript_dict['AllLines'].append((actor, line))

        if save_file:
            save_path = os.path.join('transcripts', 'season'+str(season), str(episode)+'-'+title+'.json')
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            with open(save_path, 'w+') as fout:
                json.dump(transcript_dict, fout, indent=4)

        return transcript_dict

    def craw_page_fandom(self, url, season, title):

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
    url = 'https://bigbangtrans.wordpress.com/series-9-episode-06-the-helium-insufficiency/'
    crawler.craw_page_wordpress(url, 0, 0, 'junk')


# elif p.em is not None:
            #     if p.em.string is not None:
            #         actor = "Scene"
            #         line = p.em.string
            #     else:
            #         #print(p.contents)
            #         
            #         #content = str(p)
            #         #content.replace(" ", "")
            #         #content.replace("\n", "")
            #         #content.replace("\t", "")
            #         #print(content,'\n')
            #         ##for item in p.span:
            #         #    #print(type(item))
            #         ##    print("@", item.string)
            #         #for known_name in transcript_dict.keys():
            #         #    regex = ">"+known_name+":(.+)</span"
            #         #    match = re.findall(regex, content)
            #         #    print('@',match,'\n')
            #         print("WARNING: Give up ", p)
            #         #    print()
            #         continue