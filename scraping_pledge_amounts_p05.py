#!/usr/bin/env python3
import pandas as pd
import glob
import numpy as np
from sklearn.preprocessing import LabelEncoder
from pandas import Series
import math
import csv
import os
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
import time
import re
import random
from datetime import datetime
random.seed(datetime.now())

print('Comenzando a correr el script')

data_final = pd.read_csv("Data final limpia.csv",sep = ',')
urls_list = data_final["urls"].unique()
urls_list = [url[:url.find('?ref=')] + '/comments' for url in urls_list]

useless_characters = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument('--no-sandbox')

def getPageText(url):
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get(url)
    
    try:
        # Buscar elementos de la clase "pledge_amount"
        find_pledges = driver.find_elements_by_css_selector('h2.pledge__amount')
        pledge_amounts = []
        for pledge in find_pledges:
            # Para eliminar elementos que no sean los dígitos del monto de contribución
            pledge_number = re.sub("[^\d]", "", pledge.text)
            pledge_number = int(pledge_number)
            pledge_amounts.append(pledge_number)

        pledge_amounts = list(dict.fromkeys(pledge_amounts))
        pledge_amounts.sort()
    except (NoSuchElementException, StaleElementReferenceException, TimeoutException, IndexError, ValueError):
        pledge_amounts = []
    
    return pledge_amounts

print("Scraping...")

count_pledge=6815
for id_proj, url_proj in zip(data_final["id"][6815:8518], urls_list[6815:8518]):
    pledge_amounts = getPageText(url_proj)
    df_pledges = {"ids":[id_proj], "pledge_amount":[pledge_amounts]}
    data_pledges = pd.DataFrame(df_pledges)
    data_pledges.to_csv (r'data_contribuciones_p05.csv', mode = 'a', sep = ',', index = False, header=False)
    count_pledge += 1
    del data_pledges
    del df_pledges
    del pledge_amounts
    print(count_pledge)

print('Ya terminó el scraping!')
