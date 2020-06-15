"""
reference:
https://blog.csdn.net/u014510302/article/details/52766745
https://blog.csdn.net/weixin_42323343/article/details/106145187?utm_medium=distribute.pc_relevant.none-task-blog-baidujs-3
"""
import time
import json
import signal
import random
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# constants
URL = 'https://www.huya.com/22471578' #312931 邱老师, 22234269 波波， 22289663, 816515 保镖， 22471578 菠萝包
MSG_RATE = 20 # tested min 15
DATA_SET = 'data/data.json'

# global variable
start_time = 0
counter = 0
username = ''
password = ''


def load_conf():
    global username, password
    with open('conf/pass.json') as f:
        data = json.load(f)
    username = data['username']
    password = data['password']


def load_data():
    with open(DATA_SET) as f:
        data = json.load(f)
    if 'data' not in data:
        return process_data(data)
    return data['data']


def load_main_page(browser, url):
    browser.get(url)
    time.sleep(5)
    # if page is not loaded, refresh
    while True:
        try:
            browser.find_element_by_id("nav-login")
        except NoSuchElementException:
            print('cannot find login, refreshing the page')
            browser.refresh()
            time.sleep(5)
        else:
            break


def auto_login(browser, username, password):
    browser.find_element_by_id('nav-login').click()
    browser.switch_to.frame("UDBSdkLgn_iframe")
    time.sleep(3)
    browser.find_element_by_xpath('//div[@class="udb-input-item"]//input[@placeholder="手机号/虎牙号"]').send_keys(username)
    browser.find_element_by_xpath('//div[@class="udb-input-item"]//input[@placeholder="密码"]').send_keys(password)
    browser.find_element_by_id("login-btn").click()
    time.sleep(20)
    # browser.get(URL)
    browser.switch_to.default_content()


def send_msg(browser, msg):
    global counter

    while True:
        print('DEBUG: start sending msg')
        while True:
            try:
                print('DEBUG: fetch text area')
                browser.find_element_by_id('pub_msg_input')
                input_text = browser.find_element_by_id('pub_msg_input')
            except NoSuchElementException:
                print('def send_msg: cannot fetch text area, refreshing the page')
                browser.refresh()
                time.sleep(5)
            except Exception as e:
                print('def send_msg: unknown exception')
                print(e)
            else:
                break
        random_index = random.randint(0, len(msg) - 1)
        input_text.send_keys(filter_msg(msg[random_index]))
        time.sleep(1)
        send_btn = browser.find_element_by_id('msg_send_bt')
        send_btn.click()
        print('DEBUG: msg sent')
        time.sleep(MSG_RATE)
        counter += 1


def process_data(data):
    result = []
    for province in data['provinces']:
        for city in province['citys']:
            result.append(city['citysName'])

    return result


# def filter_msg(msg):
#     filtered = msg
#     if msg == '666':
#         return filtered
#     return '@' + filtered + '天气'

def filter_msg(msg):
    return msg


def keyboardInterruptHandler(signal, frame):
    global counter
    stop_time = datetime.now()
    print('Program starts at ' + str(start_time) + ', stops at ' + str(stop_time))
    print('Running duration: ' + str(stop_time - start_time).split(".")[0])
    print('Sent: ' + str(counter))
    exit(0)


signal.signal(signal.SIGINT, keyboardInterruptHandler)
start_time = datetime.now()
load_conf()
msg = load_data()
browser = webdriver.Chrome("driver/chromedriver")
load_main_page(browser, URL)
auto_login(browser, username, password)
# msg = ['666666666666666666666666666666']
send_msg(browser, msg)
#
# # close browser
# browser.close()