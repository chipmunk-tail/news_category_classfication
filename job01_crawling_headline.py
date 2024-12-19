# 241218 intel AISW Academy
#
# 사이트의 HTML에서 뉴스 헤드라인만 추출헤 csv 파일을 생성하는 코드


from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime

# News Category
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

# Create a DataFrame
df_titles = pd.DataFrame()

# Get headlines
for i in range(6):                                              # Sub_domain : 100 ~ 105
    url = 'https://news.naver.com/section/10{}'. format(i)      # OR '/10%d' %i
    resp = requests.get(url)                                    # url request == HTML
    soup = BeautifulSoup(resp.text, 'html.parser')                  # Using bs4 for HTML parsing
    title_tags = soup.select('.sa_text_strong')                 # '.sa_text_strong' == news headline class def name
    titles = []                                                 # Create empty list for save headline

    for title_tag in title_tags:                                # all headlines
        title = title_tag.text                                  # Crawling headlines
        title = re.compile('[^가-힣 ]').sub('', title)            # Repalce all to 'null' execpt "가 ~ 힣" && " "
        titles.append(title)

    df_section_titles = pd.DataFrame(titles, columns = ['titles'])  # Create columns 'titles'
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis = 'rows', ignore_index = True)

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index = False) # Change time format to 'YYYYMMDD'
                                                                # index = False == 0, 1, 2 default index = False





