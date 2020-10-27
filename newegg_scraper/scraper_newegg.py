############################ WebScraper-Newegg ################################

# Note: bh photo video is a easy website to scrape because
#       1. It does not have a captcha mechanism in place
#       2. There is a key feature table for every product

###############################################################################

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
import numpy as np

# This does not include special promotion at the top of the page (eg. Prime Day Deal on the day I wrote this: 10/13/20)
# Also does not scrape recommendations such as 'Customers shopped Amazon's Choice for...' and 'Top rated from our brands'

# Change this to your desired path
path = 'C:\\Users\\roy79\\Desktop\\Research\\product-analysis\\newegg_scraper'
os.chdir(path)
col_names = ['name', 'ne_ID', 'rating', 'num_of_rating', 'price', 
                     'about', 'feat_labels', 'feat_values']
output = open('newegg_headphones_'+time.strftime("%Y%m%d-%H%M%S")+'.csv','w',encoding='utf-8',newline='')
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

head_href = 'https://www.newegg.com'

# Apply type filter on homepage to filter out accessories
# Headphones & Accessories: select all types other than 'Accessories'
# Bluetooth headsets & Accessories: select 'Bluetooth Headset' & 'Bluetooth Stereo Headset'
category_hrefs = ['/p/pl?N=100167718%20600010970%20600010971%20600010967%20600010968%20600095437%20600010972%20600010973%20600010974%20600010975%20600010976%20600095942%20600421069%20600482781%20600476188',
                  '/p/pl?N=100167729%20600034402%20600034409']

for category_href in category_hrefs:
    
    #category_href = category_hrefs[0]
    product_href = category_href
    start_page = '&page=1'
    url = head_href+product_href+start_page
    print('###########################')
    print('Start scraping a new category: ', category_href)
    print('###########################')


    pages = [url]    
    products_skipped = []
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
                response = requests.get(url,headers=headers)
                html = response.content
                print('Page html collected')
                # Start scraping page
                soup = BeautifulSoup(html, 'lxml')    
                body = soup.find('body')
                table = body.find('div',attrs={'class':'item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell'})
                products = table.find_all('a',attrs={'class':'item-title'})
                
                if (products):
                    print('Product list successfully pulled on page', num_page_listing)            
                break
            except KeyboardInterrupt:
                output.close()
                sys.exit('Keyboard interrupt')  
            except:
                print('##################################################')
                print('Captcha error when requesting a listing page, wait 30 seconds and reattempt.')
                print('##################################################')
                time.sleep(30)
                if (num_request_attempt % 10 == 0):
                    time.sleep(300)
                continue
                
        for product in products:
            
            #product = products[0]
            prod_url = product.attrs['href']
            is_skipproduct = False
            for num_connection_attempt in range(1,101):               
                try:
                    #time.sleep((10-2)*np.random.random()+2)
                    
                    # This can be problematic as it will select the same proxies
                    proxy = None
                    if (num_connection_attempt > 1):
                        proxy = {'https': 'https://'+random.choice(proxies)}
                    prod_response = requests.get(prod_url,headers=headers,proxies=proxy,timeout=10.0)
                    prod_html = prod_response.content
                    prod_soup = BeautifulSoup(prod_html,'lxml')
                    print('Connection established for product specs')                    
                    
                    # Every product has a ne_ID, so if we cannot find it, then we have encountered a CAPTCHA
                    ne_ID = prod_soup.find('li',{'class':'is-current'})
                    ne_ID = ne_ID.em.text                    
                    
                    break
                except KeyboardInterrupt:
                    output.close()
                    sys.exit('Keyboard interrupt')                    
                except AttributeError:
                    print('##################################################')
                    print('Captcha error when requesting a product, try connect with a proxy.')
                    print('##################################################')      
                except:
                    print('Number of connections attempted', num_connection_attempt)
                    if (num_connection_attempt == 100):
                        products_skipped.append(prod_url)
                        print('Product is skipped at', prod_url)
                        is_skipproduct = True
                    continue
            if (is_skipproduct == True):
                break
            #prod_table = prod_soup.find('div',{'class':'row is-product has-side-right has-side-items'})
            
            
            name = prod_soup.find('h1',{'class':'product-title'})
            if (name is not None):
                name = name.text
            else:
                name = ' '
            
            price = prod_soup.find('li',{'class':'price-current'})
            if (price is not None):
                dollar = price.find('strong')
                cents = price.find('sup')
                if (dollar is not None):
                    dollar = dollar.text
                else:
                    dollar = ' '
                if (cents is not None):
                    cents = cents.text
                else:
                    cents = ' '
                price = dollar+cents
            else:
                price = ' '
            # This variable exists if there is a sale going on
            price_orig = prod_soup.find('span',{'class':'price-was-data'})
            if (price_orig is not None):
                price = price_orig.text
            
            feat_table = prod_soup.find_all('div', {'class':'tab-pane'})
            if (len(feat_table) == 3):
                about = feat_table[0].find('div',{'id':'arimemodetail'}).text
                feat_table = feat_table[1]
                
            elif (len(feat_table) == 2):
                feat_table = feat_table[0]
            
            # There is another elif: 2 panes and first is 'Overview', not 'Specs'
            
            feat_rows = feat_table.find_all('tr')
            if (feat_rows is not None):
                feat_labels = [row.find('th').text for row in feat_rows]
                feat_values = [row.find('td').text for row in feat_rows]
            else:
                feat_labels = ' '
                feat_values = ' '

            rating = prod_soup.find('div',{'class':'product-seller-rating'})
            if (rating is not None):
                rating_text = rating.text.split(' ')
                rating = rating_text[2][1:]
                rating_pos = rating_text[3][:-1]
                num_of_rating = rating_text[0]
            else:
                rating = ' '
                num_of_rating = ' '
            
            
            list_info = [name, ne_ID, rating, num_of_rating, price, 
                         about, feat_labels, feat_values]
            writer.writerow(list_info)
            
            
        pages.pop(0)
        
        href = '&page=' + str(num_page_listing+1)
        next_listing_url = head_href + product_href + href
        pages.append(next_listing_url)
        #print('Next page url is ', pages[0])    
        
        print('Page scraped:',num_page_listing,'\n')
        num_page_listing = num_page_listing+1
        
        #next_button = soup.find('button',{'title':'Next'})

        # I couldn't find a way to identify last page yet;
        # The browser has it so that if page# > 100, then it goes back to 100
        # However, the scraper continues getting new data after num_page_listing > 100; up to 105 as tested
        
        # Change pagesize to 96 -> total number of products increase from 3600 to 4900
        
        if (num_page_listing == 101):
            print('The program has reached the end of the listing pages. This category has been crawled.')
            break
        
print('The program has finished scraping all categories. The program will be terminated now.')
output.close()    



