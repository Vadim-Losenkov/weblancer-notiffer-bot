import time
import requests
import json

from bs4 import BeautifulSoup


with open('data.json') as file:
    data = json.load(file)

URL = 'https://www.weblancer.net/jobs/'
URL2 = 'https://www.weblancer.net/jobs/?page=2'
WHITE_LIST = data['NEW_WHITE_LIST']

def is_programming(job):
    category = job.select('div.col-sm-8.text-muted.dot_divided a.text-muted')[0].text
    return category in WHITE_LIST


def get_content():
    try:
        return requests.get(URL).content + requests.get(URL2).content
    except Exception:
        time.sleep(2)


def check_new_updates(blocks):
    stamps = tuple(int(time.time())+i for i in range(-5, 1))
    print(tuple(filter(
        lambda block: True if any(stamp == int(block.find('span', 'time_ago')['data-timestamp']) for stamp in stamps) else False,
        blocks
    )))
    return tuple(filter(
        lambda block: True if any(stamp == int(block.find('span', 'time_ago')['data-timestamp']) for stamp in stamps) else False,
        blocks
    ))
    

def get_new_jobs():
    soup = BeautifulSoup(get_content(), 'html.parser')
    blocks = soup.find_all('div', 'row click_container-link set_href')
    new_updates = check_new_updates(blocks)

    if new_updates:
        return tuple(filter(is_programming, new_updates))
        
    return None
