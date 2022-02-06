import requests
from bs4 import BeautifulSoup
import re
import json
import csv
from io import StringIO
import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
# url = "https://www.marketwatch.com/investing/stock/aapl/options"
def marketwatch_options(tinker): 
    url = "https://www.marketwatch.com/investing/stock/" +tinker+"/options"
    df = pd.read_html(url)
    option1 = df[4]
    option2 = df[5]
    option3 = df[6]
    row1 = int(option1.shape[0])
    row2 = int(option2.shape[0])
    row3 = int(option3.shape[0])

    option1.columns = ['Strike', 'Call_Price', 'Call_Chg', 'Call_Bid', 'Call_Ask', 'Call_Vol', 'Call_Int', 'Put_Strike', 'Put_Price', 'Put_Chg', 'Put_Bid', 'Put_Ask', 'Put_Vol', 'Put_Int']
    option1_useful = option1.filter(['Strike', 'Call_Price', 'Call_Bid', 'Call_Ask', 'Put_Price', 'Put_Bid', 'Put_Ask'])
    option2.columns = ['Strike', 'Call_Price', 'Call_Chg', 'Call_Bid', 'Call_Ask', 'Call_Vol', 'Call_Int', 'Put_Strike', 'Put_Price', 'Put_Chg', 'Put_Bid', 'Put_Ask', 'Put_Vol', 'Put_Int']
    option2_useful = option2.filter(['Strike', 'Call_Price', 'Call_Bid', 'Call_Ask', 'Put_Price', 'Put_Bid', 'Put_Ask'])
    option3.columns = ['Strike', 'Call_Price', 'Call_Chg', 'Call_Bid', 'Call_Ask', 'Call_Vol', 'Call_Int', 'Put_Strike', 'Put_Price', 'Put_Chg', 'Put_Bid', 'Put_Ask', 'Put_Vol', 'Put_Int']
    option3_useful = option3.filter(['Strike', 'Call_Price', 'Call_Bid', 'Call_Ask', 'Put_Price', 'Put_Bid', 'Put_Ask'])
    if row1 > 30:
        option1_useful = option1_useful.iloc[row1//2-15:row1//2+15].reset_index(drop=True)
    if row2 > 30:
        option2_useful = option2_useful.iloc[row2//2-15:row2//2+15].reset_index(drop=True)
    if row3 > 30:
        option3_useful = option3_useful.iloc[row3//2-15:row3//2+15].reset_index(drop=True)

    return [option1_useful, option2_useful, option3_useful]

#exp_2_11.columns
# [(  'Unnamed: 0_level_0', 'Strike  Strike'),
#  (               'Calls',           'Last'),
#  (               'Calls',            'Chg'),
#  (               'Calls',            'Bid'),
#  (               'Calls',            'Ask'),
#  (               'Calls',            'Vol'),
#  ('Expires Feb 11, 2022',      'Open Int.'),
#  ('Expires Feb 11, 2022',         'Strike'),
#  ('Expires Feb 11, 2022',           'Last'),
#  (                'Puts',            'Chg'),
#  (                'Puts',            'Bid'),
#  (                'Puts',            'Ask'),
#  (                'Puts',            'Vol'),
#  (                'Puts',      'Open Int.')]