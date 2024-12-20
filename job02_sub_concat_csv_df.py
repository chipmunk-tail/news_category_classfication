# 241220 intel AISW Academy
#
# Concat dataframe

import pandas as pd
import numpy as np
import time
import datetime

# Open csv files
df_Pol = pd.read_csv('./crawling_data/naver_headline_news_Politics_20241219.csv')
df_Eco_Soc = pd.read_csv('./crawling_data/naver_headline_news_Economic_Social_20241219.csv')
df_Cul_Wor = pd.read_csv('./crawling_data/naver_headline_news_Culture_World_20241219.csv')
df_IT = pd.read_csv('./crawling_data/naver_headline_news_IT_20241219.csv')

# print(df_Pol)

# concat dataframes
df_result = pd.concat([df_Pol, df_Eco_Soc, df_Cul_Wor, df_IT])
print(df_result.head())

# Save csv
df_result.to_csv('./crawling_data/naver_headline_news_result_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index = False) # Change time format to 'YYYYMMDD'
                                                                # index = False == 0, 1, 2 default index = False






































