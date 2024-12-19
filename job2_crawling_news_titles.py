# 241219 intel AISW Academy
#
# Crawling news headline with 'selenium' and 'webdriver_manager'


from requests import options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import re
import time
import datetime


# Setting
options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')

# Webdriver setting
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service = service, options = options)


# Target url
url ='https://news.naver.com/section/100'
driver.get(url)
button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'            # button path


# Show more button macro
for i in range(15):
    time.sleep(0.5)                                             # delay 0.5s to create button
    driver.find_element(By.XPATH, button_xpath).click()         # send click

# default headline = 42 EA, show more = 36 EA
for i in range(1, 98):
    for j in range(1, 7):
        title_xpath = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(i,j)
        try:
            title = driver.find_element(By.XPATH, title_xpath).text
            print(title)
        except:
            print(i, j)                                         # ignore wrong path

time.sleep(10)                                                  # delay 10s
driver.close()                                                  # close browser




# HTML Pattern
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[1]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[2]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[3]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[4]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[5]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[6]/div/div/div[2]/a/strong'
# .
# '//*[@id="newsct"]/div[4]/div/div[1]/div[2]/ul/li[1]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[2]/ul/li[2]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[1]/div[2]/ul/li[3]/div/div/div[2]/a/strong'
# .
# .
# '//*[@id="newsct"]/div[4]/div/div[1]/div[10]/ul/li[5]/div/div/div[2]/a/strong'
#
#
# '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(i, j)
#



