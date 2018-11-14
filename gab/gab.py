import random
import requests
from agents import AGENTS
from bs4 import BeautifulSoup
from pprint import pprint
import os
import json
import math
from mydb import *
from selenium import webdriver
import time
import re

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
    base_url = "https://gab.com/"
    data = load_data("data.json")
    total = 0

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('headless')
    options.add_argument('window-size=1366x768')

    browser = webdriver.Chrome(executable_path="chromedriver.exe", options=options)

    try:
        for acc in config['accounts']:
            browser.get(base_url + acc)
            time.sleep(5)
            page_source = str(browser.page_source)
            soup = BeautifulSoup(page_source, 'html.parser')

            soup_str = str(soup)
            reg_str='followers">([0-9,]+)'

            ok = re.search(reg_str, soup_str)
            followers = 0
            if ok:
                followers = int(ok.group(1).replace(",", "").strip())

            total += followers
            data[str(acc)] = int(followers)
        total = int(math.ceil(total / 100.00) * 100.00)
    except:
        total = data["total"]
    if total < 1000:
        total = 1000
    data["total"] = total
    print("[*] GAB TOTAL: {}".format(total))
    save_new_data(data, "data.json")
    db_save("social_stats/num_gab", total)