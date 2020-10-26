######################## WebScraper-Walmart ###########################



# =============================================================================
# Amazon Search Results Structure
# body
# ->div, 'id':'search'
# ->div, 'class':'s-desktop-width-max s-desktop-content sg-row'
# ->div,
# ->div, 'class':'sg-col-inner'
# ->span, 'data-component-type':'s-search-results'
# 
# product container: div, 'data-component-type':'s-search-result'
#                     ->div, 'class':'sg-col-inner'
#                     ->span,
#                     (->div, 'data-component-type':'s-impression-logger'
#                     ->div,)
#                     ->div,
#                     ->div, 'class':'a-section a-spacing-medium'
#                     
# - image: span, 'data-component-type':'s-product-image'
#         ->a, 'class':'a-link-normal s-no-outline'
#         ->div, 'class':'a-section aok-relative s-image-square-aspect'
#         ->img, 'src'.link
# 
# - title: div, 'class':'a-section a-spacing-none a-spacing-top-small'
#         ->h2, 'class':'a-size-mini a-spacing-none a-color-base s-line-clamp-4'
#         ->a, 'class':'a-link-normal a-text-normal'
#         ->span, 'class': 'a-size-base-plus a-color-base a-text-normal'
#         
# - rating: div, 'class':'a-section a-spacing-none a-spacing-top-micro'
#         ->div, 'class':'a-row a-size-small'
#         ->span, 'aria-label':this label is the rating
# 
#     - Number of ratings: span, 'aria-label':this label is the number of ratings
# 
# - price: div, 'class':'a-section a-spacing-none a-spacing-top-small'
#         ->div, 'class':'a-row a-size-base a-color-base'
#         ->div, 'class':'a-row'
#         ->a, 'class':'a-size-base a-link-normal a-text-normal'
#         ->span, 'class':'a-price'
#         ->span, 'class':'a-offscreen'.text
# 
# 
# - next page: div,'class':'a-section a-spacing-none s-result-item s-flex-full-width s-widget'
#             ->span,
#             ->div, 'class':'a-section a-spacing-none a-padding-base'
#             ->div, 'class':'a-text-center'
#             ->ul, 'class':'a-pagination'
#             ->li, 'class':'a-last'
#             ->a, 'href': this is the link
# =============================================================================

from bs4 import BeautifulSoup
import requests
import random
import os
import csv
from urllib3.exceptions import MaxRetryError
from urllib3.exceptions import ProxyError
from requests import Timeout
import sys
import time

# This does not include special promotion at the top of the page (eg. Prime Day Deal on the day I wrote this: 10/13/20)
# Also does not scrape recommendations such as 'Customers shopped Amazon's Choice for...' and 'Top rated from our brands'

# Change this to your desired path
os.chdir('C:\\Users\\rs\\Desktop\\MScA\\Quarter 1\\msca31012\\Final Project\\product-analysis\\walmart_scraper')
col_names = ['name', 'wm_ID', 'rating', 'num_of_rating', 'price', 
                     'feat_labels', 'feat_values', 'about_text', 'about_details']
output = open('walmart_headphones.csv','w',encoding='utf-8',newline='')
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

head_href = 'https://www.walmart.com'
#product_href = '/s?k=mattress'

# change this to the category (laptops, headphones, etc.) of your choice
product_href = '/browse/headphones/headphones/3944_133251_1095191_4480?'
# start with page 2 because page 1 needs a different parsing method
start_page = 'page=1'
url = head_href+product_href+start_page

pages = [url]

# Page 1 needs a different parsing,
num_page_listing = 1



while (pages):
    url = pages[0]
    print('###########################')
    print('Start scraping listing page', num_page_listing)
    print('The url is', url)
    #print('Sleep for 3 seconds between each listing page')
    #time.sleep(3)
    headers['User-Agent'] = random.choice(user_agents)        
    
# =============================================================================
#     # Connect to a new IP address
#     for num_connection_attempt in range(1,101):
#         try:
#             print('Number of connections attempted', num_connection_attempt)
#             
#             # This can be problematic as it will select the same proxies
#             proxy = {'https': 'https://'+random.choice(proxies)}
#             
#             print('Proxy used:', proxy)
#             # This is here because I cannot find a stable proxy;
#             # proxy = {'https': 'https://176.196.225.54:1088'}
# 
#             response = requests.get(url, headers = headers, proxies = proxy, timeout=10.0)
#             print('Response retrieved', response)
#             html = response.content
#             print('Connection established')
#             break
#         except (OSError, MaxRetryError, ProxyError, Timeout) as e:
#             print(e)
#             #print(e)
#             if (num_connection_attempt == 100):
#                 output.close()
#                 sys.exit(0)
#             continue   
# =============================================================================

    #url = 'https://www.walmart.com/browse/electronics/wireless-and-bluetooth-headphones/3944_133251_1095191_1230614_1230478?&page=3'    
    for num_request_attempt in range(1,101):
        try:   
            response = requests.get(url,headers=headers)
            html = response.content
            if ('Forbidden' in str(html)):
                output.close()
                print('You have reached the end of the listing pages. This category has been crawled. The program will terminate now.')
                sys.exit(0)
         
            # Start scraping page
            soup = BeautifulSoup(html, 'lxml')    
            body = soup.find('body')
            table = body.find('ul',attrs={'data-automation-id':'search-result-gridview-items'})
            print('Page html collected')
            break
        except:
            print('##################################################')
            print('Captcha error, wait 30 seconds and reattempt.')
            print('##################################################')
            time.sleep(30)
            continue
        
    products = table.find_all('a',attrs={'data-type':'itemTitles'})
    
    
    if (products):
        print('Product list successfully pulled on page', num_page_listing)
            
        
    
    # PROBLEM: The page pulled looks different from the page appears in Chrome
    
    for product in products:
        
        prod_url = head_href+product.attrs['href']
        #print(prod_url)


        try:
            prod_response = requests.get(prod_url,headers=headers)
            prod_html = prod_response.content
            prod_soup = BeautifulSoup(prod_html, 'lxml')
            primary_info = prod_soup.find('div',{'class':'hf-Bot'})
            name = primary_info.find('h1',{'itemprop':'name'}).text
        except:
            print('##################################################')
            print('Captcha error, try connect with a proxy.')
            print('##################################################')
                # Connect to a new IP address
            for num_connection_attempt in range(1,101):
                try:
                    print('Number of connections attempted', num_connection_attempt)
                    
                    # This can be problematic as it will select the same proxies
                    proxy = {'https': 'https://'+random.choice(proxies)}
                    
                    #print('Proxy used:', proxy)
                    # This is here because I cannot find a stable proxy;
                    # proxy = {'https': 'https://176.196.225.54:1088'}
                    prod_response = requests.get(prod_url, headers = headers, proxies = proxy, timeout=10.0)
                    prod_html = response.content
                    prod_soup = BeautifulSoup(prod_html, 'lxml')
                    primary_info = prod_soup.find('div',{'class':'hf-Bot'})
                    name = primary_info.find('h1',{'itemprop':'name'}).text
                    
                    
                    print('Connection established')
                    break
                except:
                    #print(e)
                    #print(e)
                    #if (num_connection_attempt == 100):
                    #   output.close()
                    #   sys.exit(0)
                    continue
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
        
        features = prod_soup.find('div',{'class':'btf-content'})
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
            
    
    ###########################################################
    # TODO
    # 1. Turn img link to pictures
    # 2. Save to json
    # 3. Turn to next page
    #   a. How to parse the href to point to next page
    #   b. Write all the results
    ###########################################################
        
    pages.pop(0)
    
    href = 'page=' + str(num_page_listing+1)
    next_listing_url = head_href + product_href + href
    pages.append(next_listing_url)
    #print('Next page url is ', pages[0])
    
    print('Page scraped:',num_page_listing,'\n')
    num_page_listing = num_page_listing+1
output.close()


# =============================================================================
# # These codes read images from url
# # These urls do not seem to require headers or proxies
# from PIL import Image
# from io import BytesIO
# 
# img_links = ['https://m.media-amazon.com/images/I/81+pOdurwpL._AC_UL320_.jpg',
#              'https://m.media-amazon.com/images/I/81etehQ8nqL._AC_UL320_.jpg',
#              'https://m.media-amazon.com/images/I/61UXzixYkuL._AC_UL320_.jpg',
#              'https://m.media-amazon.com/images/I/81ERJyaiSuL._AC_UL320_.jpg',
#              'https://m.media-amazon.com/images/I/81HrfTqoaqL._AC_UL320_.jpg',
#              'https://m.media-amazon.com/images/I/91aiZs3HDbL._AC_UL320_.jpg',
#              'https://m.media-amazon.com/images/I/71PYFiUWJTL._AC_UL320_.jpg',
#              'https://m.media-amazon.com/images/I/81sqVLnXWDL._AC_UL320_.jpg',
#              'https://m.media-amazon.com/images/I/513klQX5zdL._AC_UL320_.jpg',
#              'https://m.media-amazon.com/images/I/81NSfScVP4L._AC_UL320_.jpg',
#              'https://m.media-amazon.com/images/I/81+pOdurwpL._AC_UL320_.jpg',
#              'https://m.media-amazon.com/images/I/81etehQ8nqL._AC_UL320_.jpg',]
# 
# imgs = []
# for img_link in img_links:
#     response = requests.get(img_link, headers=headers)
#     imgs.append(Image.open(BytesIO(response.content)))
# =============================================================================






