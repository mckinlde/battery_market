########################################################################################################################

from time import sleep
from bs4 import BeautifulSoup
import requests
import re
import mysql.connector
import smtplib
from email.mime.text import MIMEText
import datetime
from datetime import date


########################################################################################################################
# FUNCS
########################################################################################################################


def get_body(soup: BeautifulSoup):
    postingbody = soup.find('section', attrs={'id': 'postingbody'})
    return str(postingbody)


def retrieve(url: str):
    """retrieves content at the specified url"""
    print("*", url)
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    r = requests.get(url, headers=header, verify=False, timeout=5)
    sleep(1)
    soup = BeautifulSoup(r.text, "lxml")

    return soup


def get_odo(soup: BeautifulSoup):
    attrgroup = soup.findAll('p', attrs={'class': "attrgroup"})
    attrs = str(attrgroup)
    startText = attrs.find('odometer: <b>')
    if startText == -1:
        return ''
    sliceText = attrs[startText + 13:]
    endNum = sliceText.find('</b>')
    odo = sliceText[:endNum]
    return odo


def get_title(soup: BeautifulSoup):
    title = 'not found'
    span = soup.find("span", id="titletextonly")
    if span != None:
        title = span.text
        # scrub emojis
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        title = emoji_pattern.sub(r'', title)  # no emoji
        title = re.sub(r'[^\x00-\x7f]', r'', title)
    return title


def get_attrs(soup: BeautifulSoup):
    attrs = {}
    attrgroup = soup.findAll('p', attrs={'class': "attrgroup"})
    mmy = soup.find('p', attrs={'class': 'attrgroup'})
    return mmy

url_test = 'https://www.batteryjunction.com/samsung-inr18650-25r.html'

soup_test = retrieve(url_test)

#print(soup_test)

def get_price(soup: BeautifulSoup): # returns as '$x.xx'

    price = soup.find("div", class_="sale-price")
    #div class="sale-price"
    #<div class="eci-price-units">$3.95/unit</div>
    amount = price.text
    return amount


test_price = get_price(soup_test)

print(test_price)



### get all battery listings under 18650 size category
url_test = 'https://www.batteryjunction.com/18650.html'

soup_test = retrieve(url_test)


def get_url_titles(soup: BeautifulSoup):
    divs = soup.find_all('div', class_="details")
    urls = []
    titles = []
    for _ in divs:
        a = _.find('a')
        urls.append('https://www.batteryjunction.com/' + a['href'])
        titles.append(a.text)
    return urls, titles

urls, titles = get_url_titles(soup_test)

print(urls)
print(titles)

def get_nextPage(soup: BeautifulSoup):
    nextPage = soup.find()


## Main:

#1] get all URL's on first page

root = retrieve('https://www.batteryjunction.com/18650.html')


#2] start asynch process to get rest of pages
    #2a] get next page link
    #2b] get listings on page
    #2c] save to listingUrl_list list

#3] start asynch process to get prices of batteries
    #3a] get details of all listings
urls, titles = get_url_titles(root)
prices = []
for _ in urls:
    prices.append(get_price(retrieve(_)))

    #3b] save to DB

import csv
with open('eggs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

    spamwriter.writerow(['urls', 'titles', 'prices'])
    for idx, val in enumerate(urls):
        print(idx, val)
        spamwriter.writerow([urls[idx], titles[idx], prices[idx]])

    #3c] update listingUrl list, move to next if it exists, else wait for output from rest_of_pages process