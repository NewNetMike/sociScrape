import random
import requests
from agents import AGENTS
from bs4 import BeautifulSoup
from pprint import pprint
import os
import json
import math
from mydb import *

directory = os.path.dirname(os.path.realpath(__file__))

def load_data(file):
    file = directory + "/" + file
    if not os.path.isfile(file):
        with open(file, "w") as f:
            f.writelines("{}")

    with open(file) as f:
        return json.load(f)

def save_new_data(data, file):
    file = directory + "/" + file
    with open(file, 'w') as fp:
        json.dump(data, fp, indent=4)

def make_request(url, retry=0):
    if retry > 3:
        return None
    headers = {"User-Agent": random.choice(AGENTS)}
    r = requests.get(url=url, headers=headers)

    if r.status_code != 200:
        if r.status_code == 404:
            return 404
        if r.status_code == 403:
            retry += 1
            return make_request(url, retry)
        elif "/429.php" in r.url:
            retry += 1
            return make_request(url, retry)
            #print("[-] Bad Request")
    else:
        #print("[+] Successful Request")
        pass
    return r

def go(config):
    base_url = "https://mastodon.social/@"
    data = load_data("data.json")
    total = 0
    try:
        for acc in config['accounts']:
            r = make_request(base_url + acc)
            soup = BeautifulSoup(r.content, 'html.parser')
            #print(soup)

            followers = int(soup.find_all("div", {"class": "counter"})[2].find("a")["title"].replace(",", ""))
            #print(followers)

            #print("{} has {} followers".format(acc, followers))
            total += followers
            data[str(acc)] = int(followers)
        total = int(math.ceil(total / 100.00) * 100.00)
    except:
        total = data["total"]
    if total < 1000:
        total = 1000
    data["total"] = total
    print("[*] MASTODON TOTAL: {}".format(total))
    save_new_data(data, "data.json")
    db_save("social_stats/num_mastodon", total)