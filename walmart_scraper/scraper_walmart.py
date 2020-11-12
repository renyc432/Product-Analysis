######################## WebScraper-Walmart ###########################
from bs4 import BeautifulSoup
import requests
import random
import os
import csv
#from urllib3.exceptions import MaxRetryError
#from urllib3.exceptions import ProxyError
#from requests import Timeout
#from datetime import datetime
import sys
import time
from selenium import webdriver


# This does not include special promotion at the top of the page (eg. Prime Day Deal on the day I wrote this: 10/13/20)
# Also does not scrape recommendations such as 'Customers shopped Amazon's Choice for...' and 'Top rated from our brands'

# Change this to your desired path
path = 'C:\\Users\\roy79\\Desktop\\Research\\product-analysis\\walmart_scraper'
os.chdir(path)
col_names = ['name', 'wm_ID', 'rating', 'num_of_rating', 'price', 
                     'feat_labels', 'feat_values', 'about_text', 'about_details']
output = open('walmart_headphones_'+time.strftime("%Y%m%d-%H%M%S")+'.csv','w',encoding='utf-8',newline='')
writer = csv.writer(output)
writer.writerow(col_names)

# Move these to a setting file
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
}

# Some US https proxies; need to be updated before run every time
# https://hidemy.name/en/proxy-list/?country=US&maxtime=5000&type=s&anon=34#list
proxies = ['104.198.125.34:3128',
           '169.57.157.148:80',
           '117.211.100.22:3128',
           '111.93.30.66:3128',
           '159.203.84.241:3128',
           '203.99.131.204:3129',
           '189.203.74.143:3128',
           '14.139.87.36:3128',
           '117.53.47.209:1616',
           '64.227.107.38:3128',
           '169.57.157.146:8123',
           '169.57.157.148:8123',
           '169.57.157.148:25']
    
# Rotate user agent to avoid captcha
user_agents = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36']


def sel_get_url(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    driver = webdriver.Chrome(path+'\\chromedriver.exe', options=options)
    driver.get(url)
    html = driver.page_source
    return html


head_href = 'https://www.walmart.com'
#product_href = '/s?k=mattress'

# change this to the category (laptops, headphones, etc.) of your choice
category_hrefs = ['/browse/electronics/wireless-and-bluetooth-headphones/3944_133251_1095191_1230614_1230478?',
                 '/browse/electronics/over-ear-and-on-ear-headphones/3944_133251_1095191_1230614_1230477?',
                 '/browse/electronics/earbuds-and-in-ear-headphones/3944_133251_1095191_1230614_1230476?',
                 # Sports Headphones; skip; only 88 products and highly likely overlap with bluetooth headphones
                 #'/browse/electronics/sports-headphones/3944_133251_1095191_1230614_1231506?povid=1095191+%7C+2018-04-30+%7C+Shop%20by%20Category%20Sports%20Headphones?',
                 # Kids' headphones: skip; likely have a totally different set of features and focus more on looks which we are not analyzing
                 #'/browse/electronics/kids-headphones/3944_133251_1095191_1230614_1230480?',
                 # Waterproof headphones: only 12 products; doesn't make sense as a category anymore, many headphones are water proof/resistant these days
                 # '/browse/shop-headphones-by-type/waterproof-headphones/3944_133251_1095191_1230614_8436721?'
                 '/browse/electronics/pro-dj-headphones/3944_96469_1230614_1231507?'
                 ]

products_skipped = []

for category_href in category_hrefs:
    
    category_href = category_hrefs[0]
    product_href = category_href
    start_page = 'page=1'
    url = head_href+product_href+start_page
    print('###########################')
    print('Start scraping a new category: ', category_href)
    print('###########################', '\n')

    pages = [url]    
    num_page_listing = 1

    while (pages):
        url = pages[0]
        print('###########################')
        print('Start scraping listing page', num_page_listing)
        print('The url is', url)
        #print('Sleep for 3 seconds between each listing page')
        #time.sleep(3)
        headers['User-Agent'] = random.choice(user_agents)
    
        for num_request_attempt in range(1,101):
            try:
                #response = requests.get(url,headers=headers)
                #html = response.content
                
                html = sel_get_url(url)
                
                # use a separate except to catch sys.exit()
                if ('Forbidden' in str(html)):
                    output.close()
                    print('You have reached the end of the listing pages. This category has been crawled. The program will terminate now.')
                    sys.exit(0)
                    
                # Start scraping page
                soup = BeautifulSoup(html, 'lxml')    
                body = soup.find('body')
                table = body.find('ul',attrs={'data-automation-id':'search-result-gridview-items'})               
                products = table.find_all('a',attrs={'data-type':'itemTitles'})
                
                if (products):
                    print('Product list successfully pulled on page', num_page_listing)
                break
            except SystemExit:
                sys.exit(0)
            except KeyboardInterrupt:
                output.close()
                sys.exit('Keyboard interrupt')
            except:
                print('##################################################')
                print('Captcha error when requesting a listing page, wait 30 seconds and reattempt.')
                time.sleep(30)
                if (num_request_attempt % 10 == 0):
                    time.sleep(300)
                continue
                                  
        # PROBLEM: The page pulled looks different from the page appears in Chrome (Javascript issue, can be reslved by using selenium)
        for product in products:
            prod_url = head_href+product.attrs['href']
            
            #prod_url = 'https://www.walmart.com/ip/SEGMART-Wireless-Bluetooth-Earbuds-Mic-5-0-Headset-Charging-Case-Auto-Pairing-Hi-Fi-Stereo-Sound-Earbuds-Sports-Earphone-iPhone-XS-Samsung-Black-S104/575479570'
            
            is_skipproduct = False
            for num_connection_attempt in range(1,101):
                try:
                    print('Number of connections attempted', num_connection_attempt)
                    proxy = None
                    if (num_connection_attempt > 1):
                        # This can be problematic as it will select the same proxies
                        proxy = {'https': 'https://'+random.choice(proxies)}
                    prod_response = requests.get(prod_url,headers=headers,proxies=proxy,timeout=10.0)
                    print('prod_response')
                    prod_html = prod_response.content
                    print('prod_html')
                    prod_soup = BeautifulSoup(prod_html, 'lxml')
                    print('prod_soup')
                    primary_info = prod_soup.find('div',{'class':'hf-Bot'})
                    print('primary_info')
                    name = primary_info.find('h1',{'itemprop':'name'}).text
                    features = prod_soup.find('div',{'class':'btf-content'})
                    #print(name)
                    #print(features)
                    break
                except KeyboardInterrupt:
                    output.close()
                    sys.exit('Keyboard interrupt')
                except:
                    if (num_connection_attempt == 1):
                        print('##################################################')
                        print('Captcha error when requesting a product, try a proxy.')
                    if (num_connection_attempt == 100):
                        products_skipped.append(prod_url)
                        print('Product is skipped at', prod_url)
                        is_skipproduct = True
# =============================================================================
#                         print('Sleep for 5 minutes')
#                         time.sleep(300)
# =============================================================================
                    continue
                
            if (is_skipproduct == True):
                continue
            
            wm_ID = primary_info.find('div',{'class':'valign-middle secondary-info-margin-right copy-mini display-inline-block wm-item-number'})
            if (wm_ID is not None):
                wm_ID = wm_ID.text
            else:
                wm_ID = ' '
            
            rating = primary_info.find('span',{'itemprop':'ratingValue'})
            if (rating is not None):
                rating = rating.text
            else:
                rating = ' '
            
            num_of_rating = primary_info.find('span',{'class':'stars-reviews-count-node'})
            if (num_of_rating is not None):
                num_of_rating = num_of_rating.text
            else:
                num_of_rating =' '
            
            price = primary_info.find('span',{'class':'price display-inline-block arrange-fit price price--stylized'})
            if (price is not None):
                price = price.find_next('span').text
            else:
                price = ' '
            
            feature_hl = features.find('ul',{'class':'SpecHighlights-list Grid text-left'})
            feat_labels = ' '
            feat_values = ' '
            if (feature_hl is not None):
                feature_hl_label = feature_hl.find_all('div',{'class':'SpecHighlights-list-label'})
                feature_hl_value = feature_hl.find_all('div',{'class':'SpecHighlights-list-value'})
                # parse feature_hl_label, feature_hl_value
           
                feat_labels = [lab.text for lab in feature_hl_label]
                feat_values = [val.text for val in feature_hl_value]
            
            about_text = prod_soup.find('div',{'class':'about-desc about-product-description xs-margin-top'})
            if (about_text is not None):
                about_list = about_text.find_next('ul')
                about_text = about_text.text
                
            # about_list does not always exist and can exist at multiple places
            if (about_list is not None and about_list != []):
                about_list = about_list.find_all('li')
            else:
                about_list = about_list.find_next('ul')
                if (about_list is not None and about_list != []):
                    about_list = about_list.find_all('li')
            about_details = []
            about_details = [detail.text for detail in about_list]
            
            list_info = [name, wm_ID, rating, num_of_rating, price, 
                         feat_labels, feat_values, about_text, about_details]
            writer.writerow(list_info)
                
        pages.pop(0)
        
        href = 'page=' + str(num_page_listing+1)
        next_listing_url = head_href + product_href + href
        pages.append(next_listing_url)
        #print('Next page url is ', pages[0])
        
        print('Page scraped:',num_page_listing,'\n')
        num_page_listing = num_page_listing+1
    
with open('products_skipped'+time.strftime("%Y%m%d-%H%M%S")+'.csv','w') as prod_skipped_out:
                for prod in products_skipped:
                    prod_skipped_out.write('%s\n' % prod)
output.close()


