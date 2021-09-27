import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import time
import os
from os import path
from tqdm import tqdm

import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
import statsmodels.api as sm
import bs4 as bs
#import seaborn as sns
from scipy import stats

from selenium import webdriver


import requests
import urllib.request

from selenium.webdriver.chrome.options import Options

#URL of condos for sale in the city of Toronto
#url = 'https://www.kijiji.ca/b-condo-for-sale/city-of-toronto/'
baseurl = 'https://www.realmaster.com/en/sold-price/Toronto-ON'
#baseurl = 'https://www.realmaster.com/en/for-sale/Toronto-ON'
baseForToronto = '/c643l1700273'
pageNos = '?page='
#url = 'https://www.kijiji.ca/b-condo-for-sale/city-of-toronto/c643l1700273'


adurl = []
listing = []
urlToSave = []
title = []

prices = []
description = []
location = []
bedrooms = []
bathrooms = []
parking = []
sqft = []
levels = []
balc = []

datePosted = []
features = []
linksFromText = []
adId = []


savePoints = [10,1000,2000,3000,4000,5000,6000,7000]
import requests

headers = {
    'authority': 'www.realmaster.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.realmaster.com/en/for-sale/Toronto-ON?page=0',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cookie': 'locale=en; _ga=GA1.2.79439591.1630541321; _gid=GA1.2.1287870059.1630695941; cmate.sid=a5S2MMfX7APUG73PSTlB3W0BXQgiBoDjqUijdPJrbqEmRs9axJRPMauZkt4x6m21; wk=D1HJU55dq2XZ8THnPmtJN; cityhist=%5B%7B%22city%22%3A%22Toronto%22%2C%22prov%22%3A%22Ontario%22%2C%22pr%22%3A%22ON%22%2C%22url%22%3A%22%2Ffor-sale%2FToronto-ON%22%7D%5D; _gat_gtag_UA_75789502_1=1',
}

params = (
    ('d', 'https://www.realmaster.com/en/for-sale/Toronto-ON?page=0'),
)

#response = requests.get('https://www.realmaster.com/en/toronto-on/85-beechborough-ave/beechborough-greenbrook-TRBW5335180', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.realmaster.com/en/toronto-on/85-beechborough-ave/beechborough-greenbrook-TRBW5335180?d=https://www.realmaster.com/en/for-sale/Toronto-ON?page=0', headers=headers)

def getAttr(key):
    adType = soup.find('span', text = key, attrs={'class' : 'summary-label'}) #Stats div
    #Gets sibling which is next to the summary label dom
    return adType.nextSibling.get_text()

def getAdId(advt):
    advtList = advt.split("/")
    adlen = len(advtList)
    return advtList[adlen-1]


def saveToDisk(i):
    print("saving ***")
    name='realmaster'+str(i)+'.csv'
    d = {'Price':prices,
          'Location':location, 'Floor':levels,
          'Bedrooms':bedrooms, 'Bathrooms':bathrooms,
          'Parking':parking, 'Balcony': balc, 'Square feet': sqft}
    df = pd.concat([pd.Series(v, name=k) for k, v in d.items()], axis=1)
    df.to_csv(name,index=False)
    resetAll()

def getDetails(urls):

    #urls = urls[6766:]
    #print(len(urls))

    i =0;
    try:
        for j in tqdm(range(len(urls)), position = 0, leave = True):
            url = urls[j]

            url = url.rstrip('\n')
            listDetails = ""
            listDetailsTwo = []
            #session = requests.Session()
            response = requests.get(url, headers=headers)
            if (response.ok):
                #response.raise_for_status()
                #driver.get(url)
                #soup = BeautifulSoup(driver.page_source, "html.parser")
                soup = BeautifulSoup(response.text, "html.parser")

                try:
                    adType = soup.find('span', text = 'Type', attrs={'class' : 'summary-label'})
                    #print(adType)
                    #Gets sibling which is next to the summary label dom
                    adType = adType.nextSibling.get_text()
                    #adType = getAttr("Type")
                    print(adType + "\n")
                    if (adType == "Residential Apartment"):
                        adLevel = soup.find('span', text = 'Level', attrs={'class' : 'summary-label'})
                        adLevel = adLevel.nextSibling.get_text()
                        levels.append(adLevel)
                        print("Level: " + adLevel + "\n")

                        adBalc = soup.find('span', text = 'Balcony', attrs={'class' : 'summary-label'})
                        adBalc = adBalc.nextSibling.get_text()
                        balc.append(adBalc)
                        print(adBalc + "\n")

                        #adPrice = soup.select_one("span[class*=currentPrice-2842943473]").get_text() #Price of condo
                        adPrice = soup.find('span', attrs={'class' : 'detail-price'}).get_text()
                        print(adPrice + "\n")
                        prices.append(adPrice)

                        adLocation = soup.find('span', attrs={'class' : 'listing-prop-address'}).get_text()
                        location.append(adLocation)
                        print(adLocation + "\n")

                        adSqft = soup.find('span', attrs={'class' : 'listing-prop-sqft'}).get_text()
                        sqft.append(adSqft)
                        print(adSqft + "\n")


                        #Room info
                        rooms = soup.find_all('span', attrs={'class' : 'listing-prop-room'})
                        quantity0 = rooms[0].find('span').get_text()
                        bedrooms.append(quantity0)
                        quantity1 = rooms[1].find('span').get_text()
                        bathrooms.append(quantity1)
                        quantity2 = rooms[2].find('span').get_text()
                        parking.append(quantity2)
                        print("Parking: " + quantity2 + "\n")

                        i += 1
                    else:
                        raise Exception('Not a condo/apt!')
                    #response.close()
                    if i in savePoints:
                        saveToDisk(i)
                        #break
                    time.sleep(1) #to avoid getting timed out
                except Exception as e:
                    print(e)
        saveToDisk(i)
    except Exception as e:
        print(e)
        pass

def resetAll():
    print('cleaning')
    adId.clear()
    title.clear()
    prices.clear()
    description.clear()
    datePosted.clear()
    location.clear()
    bedrooms.clear()
    bathrooms.clear()
    sqft.clear()
    levels.clear()
    balc.clear()
    features.clear()

#Scrape the sold pages
noPages = 100
if path.exists('links.txt'):
    with open('links.txt', 'r') as f:
        linksFromText = f.readlines()
    f.close()
    # A function call to scrape the actual webpage
    getDetails(linksFromText)
# if file does not exists perform the scraping
else:
    for i in range(noPages):
        print("Scraping page " + str(i))
        url_final = baseurl+pageNos+str(i)
        response = requests.get(url_final, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        ad = soup.find_all('a', attrs={'class' : 'listing-prop box-shadow border-radius-all'})
        try:
            for link in ad:
                adlink = link['href']
                if not link.find('div', attrs={'class' : 'listing-prop-img-status toplisting'}):
                    #inter = link.find_all('span', attrs={'class' : 'listing-prop-img-status toplisting'})
                    #intersections.append(inter[0].get_text() + " / " + inter[1].get_text() + ", Toronto, ON, Canada")
                    adurl.append(adlink)
        except Exception as e:
                print(e)
        print(len(adurl))
        time.sleep(1)
    # a fuction to write the
    print("Saving links...")
    with open('links.txt', 'w') as f:
        for item in adurl:
            f.write("%s\n" % item)
    f.close()
    # a fuction to do the actual scraping
    print("Getting details of ads...")
    getDetails(adurl)
