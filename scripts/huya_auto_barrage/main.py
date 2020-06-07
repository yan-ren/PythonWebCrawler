'''
reference:
https://blog.csdn.net/u014510302/article/details/52766745
https://blog.csdn.net/weixin_42323343/article/details/106145187?utm_medium=distribute.pc_relevant.none-task-blog-baidujs-3
'''
import time
import json
import signal
import random
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# constants
URL = 'https://www.huya.com/816515' #312931 邱老师, 22234269 波波， 22289663
MSG_RATE = 15
DATA_SET = 'data/data2.json'

# global variable
start_time = 0
counter = 0


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


def auto_login(browser):
    browser.find_element_by_id('nav-login').click()
    browser.switch_to.frame("UDBSdkLgn_iframe")
    time.sleep(3)
    browser.find_element_by_xpath('//div[@class="udb-input-item"]//input[@placeholder="手机号/虎牙号"]').send_keys('**********')
    browser.find_element_by_xpath('//div[@class="udb-input-item"]//input[@placeholder="密码"]').send_keys('*********')
    browser.find_element_by_id("login-btn").click()
    time.sleep(20)
    browser.get(URL)
    browser.switch_to.default_content()


def send_msg(browser, msg):
    global counter
    print('send msg')
    while True:
        print('start sending text')
        while True:
            try:
                print('finding text area')
                browser.find_element_by_id('pub_msg_input')
                input_text = browser.find_element_by_id('pub_msg_input')
            except NoSuchElementException:
                print('cannot find input area, refreshing the page')
                browser.refresh()
                time.sleep(5)
            except Exception as e:
                print('send msg, unknown exception')
                print(e)
            else:
                break
        random_index = random.randint(0, len(msg) - 1)
        input_text.send_keys(filter_msg(msg[random_index]))
        time.sleep(1)
        send_btn = browser.find_element_by_id('msg_send_bt')
        send_btn.click()
        time.sleep(MSG_RATE)
        counter += 1


def filter_msg(msg):
    filtered = msg
    if msg == '666':
        return filtered
    return '@' + filtered + '天气'


def process_data(data):
    result = []
    for province in data['provinces']:
        for city in province['citys']:
            result.append(city['citysName'])

    return result


def keyboardInterruptHandler(signal, frame):
    global counter
    stop_time = datetime.now()
    print('Program starts at ' + str(start_time) + ', stops at ' + str(stop_time))
    print('Running duration: ' + str(stop_time - start_time).split(".")[0])
    print('Sent: ' + str(counter))
    exit(0)


# signal.signal(signal.SIGINT, keyboardInterruptHandler)
start_time = datetime.now()

msg = load_data()
browser = webdriver.Chrome("driver/chromedriver")
load_main_page(browser, URL)
# time.sleep(20)
auto_login(browser)
send_msg(browser, msg)
#
# # close browser
# browser.close()