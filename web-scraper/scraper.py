#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import sys
import shutil
import re
import threading
import os
from bs4 import BeautifulSoup as soup
from lxml.html import fromstring
from itertools import cycle
import traceback
import random

THREAD_COUNTER = 0
THREAD_MAX = 5
PROXY_POOL = None


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:100]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


def get_source(link):
    r = requests.get(link)
    if r.status_code == 200:
        return soup(r.text)
    else:
        sys.exit('[~] Invalid Response Received.')


def extract_tags(html):
    imgs = html.findAll('img')
    if imgs:
        return imgs
    else:
        sys.exit('[~] No images detected on the page.')


def handle_request(link, name, dir):
    global PROXY_POOL
    if PROXY_POOL is None:
        sys.exit('[~] Proxy pool is empty, terminate.')

    if os.path.isfile("./" + dir + "/" + name):
        print('[I] File %s exist, skip' % name)
        return

    global THREAD_COUNTER
    THREAD_COUNTER += 1

    # Get a proxy from the pool
    proxy = random.choice(tuple(PROXY_POOL))
    try:
        print('[I] Sending request using proxy %s' % proxy)
        r = requests.get(link, proxies={"http": proxy, "https": proxy}, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            f = open("./" + dir + "/" + name, 'wb')
            shutil.copyfileobj(r.raw, f)
            f.close()
            print('[*] Downloaded Image: %s' % name)
    except Exception as error:
        print('[~] Error Occurred with %s : %s' % (name, error))
        print('[I] Error using proxy %s, removed' % proxy)
        PROXY_POOL.remove(proxy)
        if len(PROXY_POOL) < 1:
            print('[I] Proxy pool is low, regenerate pool')
            PROXY_POOL = get_proxies()
        print('[I] Sending request again %s' % link)
        handle_request(link, name, dir)

    THREAD_COUNTER -= 1


def extract_url(tags):
    url_list = []
    for tag in tags:
        src = tag.get('data-src')
        if src:
            src = re.match(r"(you need some regex here)", src)
            if src:
                (link, name) = src.groups()
                url_list.append(link.replace("thumbs/", ""))
    return url_list


def download_single_thread(urls, dir):
    # create new_folder directory for storage
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, dir)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    for url in urls:
        handle_request(url, url.split('/')[-1], dir)


def download_multithreads(urls, dir):
    # create new_folder directory for storage
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, dir)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    for url in urls:
        handle_request(url, url.split('/')[-1], dir)

        _t = threading.Thread(target=handle_request, args=(url, url.split('/')[-1], dir))
        _t.daemon = True
        _t.start()

        while THREAD_COUNTER >= THREAD_MAX:
            pass


def main():
    # html = get_source('link you want')
    file_path = "source file"
    with open(file_path, "r") as f:
        contents = f.read()
        text = soup(contents, 'html.parser')

    tags = extract_tags(text)
    urls = extract_url(tags)
    global PROXY_POOL
    PROXY_POOL = get_proxies()
    # print(PROXY_POOL)
    download_single_thread(urls, 'new_folder')


if __name__ == '__main__':
    main()
