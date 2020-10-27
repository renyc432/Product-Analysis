######################## WebScraper-B&H Photo Video ###########################

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

# This does not include special promotion at the top of the page (eg. Prime Day Deal on the day I wrote this: 10/13/20)
# Also does not scrape recommendations such as 'Customers shopped Amazon's Choice for...' and 'Top rated from our brands'

# Change this to your desired path
path = 'C:\\Users\\roy79\\Desktop\\Research\\product-analysis\\bhphotovideo_scraper'
os.chdir(path)
col_names = ['name', 'wm_ID', 'rating', 'num_of_rating', 'price', 
                     'feat_labels', 'feat_values']
output = open('bhpv_headphones_'+time.strftime("%Y%m%d-%H%M%S")+'.csv','w',encoding='utf-8',newline='')
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

head_href = 'https://www.bhphotovideo.com'

category_hrefs = ['/c/buy/Wireless-Bluetooth-Headphones/ci/4947/N/3753775947',
                  '/c/buy/Headphones/ci/12572/N/3753775955',
                  '/c/buy/Earphones/ci/12574/N/3753775954',
                  '/c/buy/tv-headphones/ci/28443/N/3753775948',
                  '/c/buy/Computer-Gaming-Headsets/ci/11115/N/3753775957',
                  '/c/buy/Studio-Headphones/ci/12223/N/3753775956',
                  '/c/buy/DJ-Headphones/ci/13943/N/3753775950']

for category_href in category_hrefs:


    product_href = category_href
    start_page = '/pn/1'
    url = head_href+product_href+start_page
    
    print('###########################')
    print('Start scraping a new category: ', url)
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
                table = body.find('div',attrs={'id':'listingRootSection'})
                products = table.find_all('a',attrs={'data-selenium':'miniProductPageProductNameLink'})
                if (products):
                    print('Product list successfully pulled on page', num_page_listing)            
                break
            except:
                print('##################################################')
                print('Captcha error when requesting a listing page, wait 30 seconds and reattempt.')
                print('##################################################')
                time.sleep(30)
                if (num_request_attempt % 10 == 0):
                    time.sleep(300)
                continue
                
        for product in products:
            
            #product = products[1]
            prod_url = head_href+product.attrs['href']
            prod_specs_url = prod_url+'/specs'
    
            try:
                prod_specs_response = requests.get(prod_specs_url,headers=headers)
                prod_specs_html = prod_specs_response.content
                prod_specs_soup = BeautifulSoup(prod_specs_html,'lxml')
                print('Connection established for product specs')
    
            except KeyboardInterrupt:
                output.close()
                sys.exit('Keyboard interrupt')
            except:
                print('##################################################')
                print('Captcha error when requesting a product, try connect with a proxy.')
                print('##################################################')
                    # Connect to a new IP address
                for num_connection_attempt in range(1,101):
                    try:
                        print('Number of connections attempted', num_connection_attempt)
                        
                        # This can be problematic as it will select the same proxies
                        proxy = {'https': 'https://'+random.choice(proxies)}
                        prod_specs_response = requests.get(prod_specs_url, headers = headers, proxies = proxy, timeout=10.0)
                        prod_specs_html = prod_specs_response.content
                        prod_specs_soup = BeautifulSoup(prod_specs_html, 'lxml')
                        print('Connection established for product specs')
                        
                        break
                    except:
                        if (num_connection_attempt == 100):
                            products_skipped.append(prod_url)
                            print('Product is skipped at', prod_url)
                        continue
                continue
            
            name = prod_specs_soup.find('h1',{'data-selenium':'productTitle'})
            if (name is not None):
                name = name.text
            else:
                name = ' '
            
            bh_ID_and_mfr_ID = prod_specs_soup.find('div',{'data-selenium':'codeCrumb'})
            if (bh_ID_and_mfr_ID is not None):
                bh_ID_and_mfr_ID = bh_ID_and_mfr_ID.text
            else:
                bh_ID_and_mfr_ID = ' '
            
            price = prod_specs_soup.find('div',{'data-selenium':'pricingPrice'})
            if (price is not None):
                price = price.text         
            else:
                price = ' '
            # This variable exists if there is a sale going on
            price_orig = prod_specs_soup.find('del',{'data-selenium':'strikeThroughPrice'})
            if (price_orig is not None):
                price = price_orig.text
                
            price_ifunavail = prod_specs_soup.find('div',{'data-selenium':'pricingContainer'})
            if (price_ifunavail is not None):
                price_ifunavail = price_ifunavail.find('strong')
                if (price_ifunavail is not None):
                    price = price_ifunavail.text
            
            feat_rows = prod_specs_soup.find_all('tr',{'data-selenium':'specsItemGroupTableRow'})
            if (feat_rows is not None):
                feat_labels = [row.find('td',{'data-selenium':'specsItemGroupTableColumnLabel'}).text for row in feat_rows]
                feat_values = [row.find('td',{'data-selenium':'specsItemGroupTableColumnValue'}).find('span').text for row in feat_rows]
            else:
                feat_labels = ' '
                feat_values = ' '
        
            rating_stars = prod_specs_soup.find('span',{'data-selenium':'reviewsRatingStars'})
            if (rating_stars is not None):
                stars = rating_stars.find_all('svg')            
                stars_text = [star.attrs['class'] for star in stars]
                rating = 0
                for item in stars_text:
                    if (len(item) < 3):
                        rating = rating + 0.5
                    elif ('full' in item[2]):
                        rating = rating + 1
                    elif ('empty' in item[2]):
                        rating = rating + 0
            else:
                rating = ' '
            
            
            num_of_rating = prod_specs_soup.find('span',{'data-selenium':'reviewsNumber'})
            if (num_of_rating is not None):
                num_of_rating = num_of_rating.text
            else:
                num_of_rating = ' '
            
            list_info = [name, bh_ID_and_mfr_ID, rating, num_of_rating, price, 
                         feat_labels, feat_values]
            writer.writerow(list_info)
            
            
        pages.pop(0)
        
        href = '/pn/' + str(num_page_listing+1)
        next_listing_url = head_href + product_href + href
        pages.append(next_listing_url)
        #print('Next page url is ', pages[0])    
        
        print('Page scraped:',num_page_listing,'\n')
        num_page_listing = num_page_listing+1
        
        next_button = soup.find('a',{'data-selenium':'listingPagingPageNext'})
        if (next_button is None):
            break
        next_button = next_button.find('svg')
        if (len(next_button.attrs['class']) == 2 and 'Disabled' in next_button.attrs['class'][1]):
            print('The program has reached the end of the listing pages. This category has been crawled.')
            break
        
print('The program has finished scraping all categories. The program will be terminated now.')
output.close()    



