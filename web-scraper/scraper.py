#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import sys
import shutil
import re
import threading
import os
from bs4 import BeautifulSoup as soup

THREAD_COUNTER = 0
THREAD_MAX = 1


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


def handle_request(link, name):
    global THREAD_COUNTER
    THREAD_COUNTER += 1
    try:
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'new_folder')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        r = requests.get(link, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            f = open("./new_folder/" + name, 'wb')
            shutil.copyfileobj(r.raw, f)
            f.close()
            print ('[*] Downloaded Image: %s' % name)
    except Exception as error:
        print ('[~] Error Occured with %s : %s' % (name, error))
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


def main():
    # html = get_source('link you want')
    file_path = "your file path"
    with open(file_path, "r") as f:
        contents = f.read()
        text = soup(contents, 'html.parser')

    tags = extract_tags(text)
    urls = extract_url(tags)
    for url in urls:
        handle_request(url, url.split('/')[-1])

    # while THREAD_COUNTER >= THREAD_MAX:
    #     pass
    # for tag in tags:
    #     src = tag.get('src')
    #     if src:
    #         src = re.match(r"((?:https?:\/\/.*)?\/(.*\.(?:png|jpg)))", src)
    #         if src:
    #             (link, name) = src.groups()
    #             if not link.startswith('http'):
    #                 link = 'https://www.drivespark.com' + link
    #             _t = threading.Thread(target=requesthandle, args=(link,
    #                     name.split('/')[-1]))
    #             _t.daemon = True
    #             _t.start()
    #
    #             while THREAD_COUNTER >= THREAD_MAX:
    #                 pass
    #
    # while THREAD_COUNTER > 0:
    #     pass


if __name__ == '__main__':
    main()
