# -*- coding: utf-8 -*-
# import io
import sys
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs4
import time
#################################################
# start script
#################################################
def get_wiki_pub_url(wikiurl):
  res = requests.get(wikiurl)
  # soup = BeautifulSoup(res.text, 'html.parser')
  soup = bs4(res.content,'lxml')
  #
  title_text = soup.find('title').get_text()
  print(title_text)
  #
  # 検索箇所："table .infobox" > ?(text='外部リンク')+ > "a".href 
  info_box = soup.find("table", {"class", "infobox"})
  # print(info_box)
  _quote_tmp = info_box.find(text='外部リンク')
  # print(_quote_tmp)
  # check for a link exist
  if _quote_tmp is None :
    print('not found public link')
    return wikiurl
  _quote_tmp = info_box.find(text='外部リンク').next_element
  # print(_quote_tmp)
  link_url = _quote_tmp.a.get('href')
  print(link_url)
  return link_url

#################################################
# start script
#################################################
args = sys.argv
json_file = args[1]
json_open = open(json_file, 'r')
json_load = json.load(json_open)
# print(json_load)

json_city_array = []
json_city_array = json_load['result']
# print(json_city_array)
#
# set DataFrame
base_url = 'https://ja.wikipedia.org/wiki/'
# set DataFrame
base_url = 'https://ja.wikipedia.org/wiki/'
# df = pd.DataFrame({
#   'prefCode' : 0,
#   'cityCode' : '0',
#   'cityName' : '市区町村',
#   'wikiName' : '市区町村',
#   'bigCityFlag' : '0',
#   'cityURL'  : ''},
#   index=['00000'])
_df_cols = ['prefCode', 'cityCode', 'cityName', 'wikiName','bigCityFlag','cityURL']
df = pd.DataFrame(columns=_df_cols)
print(df)
#
for json_city in json_city_array:
  print(json_city)
  _prefCode = json_city['prefCode']
  _cityCode = json_city['cityCode']
  _cityName = json_city['cityName']
  _wikiName = json_city['wikiName']
  _bigCityFlag = json_city['bigCityFlag']
  _cityURL  = base_url +  json_city['wikiName']
  df.loc[_cityCode] = [_prefCode, _cityCode, _cityName, _wikiName, _bigCityFlag, _cityURL]
print(df)
#
for row in df.itertuples():
  if (row.cityCode != '0'):
    # print(type(row))
    # print(row['wikiURL'])
    print(row.cityName)
    # print(row.wikiURL)
    _getCityURL = get_wiki_pub_url(row.cityURL)
    df.loc[row.cityCode, 'cityURL'] = _getCityURL
    time.sleep(1)
#
print(df)
df.to_csv("outcsv_with_cityURLs.csv", index = False)
#
#EOF