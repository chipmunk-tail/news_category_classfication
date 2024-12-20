# 241219 intel AISW Academy
#
# Crawling news headline with 'selenium' and 'webdriver_manager'
# 5 Domain crawling


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

# News Category
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

# Create a DataFrame
df_titles = pd.DataFrame()

# Setting
options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')

# Webdriver setting
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service = service, options = options)


# Target domain 100 ~ 105
for i in range(6):
    url = 'https://news.naver.com/section/10{}'.format(i)
    driver.get(url)
    titles = []                                                 # Create empty list for save headline

    if i == 1:                                                  # Only domain/101 use div[5]
        button_xpath = '//*[@id="newsct"]/div[5]/div/div[2]'
    else:
        button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'

    # click macro
    for l in range(15):
        time.sleep(0.3)                                         # Delay time to create button
        driver.find_element(By.XPATH, button_xpath).click()     # set click

    # default headline = 42 EA, show more = 36 EA
    for j in range(1, 98):
        for k in range(1, 7):

            if i == 1:                                          # Only domain/101 use div[5]
                title_xpath = '//*[@id="newsct"]/div[5]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(j, k)
            else:
                title_xpath = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(j, k)

            try:
                title = driver.find_element(By.XPATH, title_xpath).text
                title = re.compile('[^가-힣 ]').sub(' ', title)        # Repalce all to 'null' execpt "가 ~ 힣" && " "
                titles.append(title)

                print(title)
            except:
                print(i, j, k)

    df_section_titles = pd.DataFrame(titles, columns = ['titles'])          # Create columns 'titles'
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis = 'rows', ignore_index = True)



time.sleep(3)                                                  # delay 3s
driver.close()                                                 # close browser

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_exam_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index = False) # Change time format to 'YYYYMMDD'
                                                                # index = False == 0, 1, 2 default index = False



# Domain pattern
#
# 100
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[1]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[2]'
#
# 101
# '//*[@id="newsct"]/div[5]/div/div[1]/div[1]/ul/li[1]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[5]/div/div[2]'
# 경제탭은 플랫이 들어가서 다르다.
#
# 102
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[1]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[2]'
#
# 103
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[1]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[2]'
#
# 104
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[1]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[2]'
#
# 105
# '//*[@id="newsct"]/div[4]/div/div[1]/div[1]/ul/li[1]/div/div/div[2]/a/strong'
# '//*[@id="newsct"]/div[4]/div/div[2]'



