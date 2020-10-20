######################## WebScraper-Amazon ###########################


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

# This does not include special promotion at the top of the page (eg. Prime Day Deal on the day I wrote this: 10/13/20)
# Also does not scrape recommendations such as 'Customers shopped Amazon's Choice for...' and 'Top rated from our brands'


os.chdir('C:\\Users\\rs\\Desktop\\MScA\\Quarter 1\\MSCA 31012 4\\HW1')

col_names = ['Product','Price','Rating','Number of Ratings','Image Link']
output = open('products.csv','w',encoding='utf-8',newline='')
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
proxies = ['176.196.225.54:1088',
           '139.99.105.5:80',
           '169.57.157.148:8123',
           '162.241.115.246:80',
           '108.61.75.207:8080',
           '209.190.32.28:3128',
           '157.230.81.64:3128',
           '159.203.84.241:3128',
           '117.211.100.22:3128',
           '117.53.47.209:1616',
           '111.93.30.66:3128']
    
# Rotate user agent to avoid captcha
user_agents = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36']

head_href = 'https://www.amazon.com'
#product_href = '/s?k=mattress'
product_href = '/s?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565108'
start_page = '&page=2'
url = head_href+product_href+start_page

pages = [url]

# Page 1 needs a different parsing,
# Assume for now we start at page 2
numPage = 2
while (pages):
    url = pages[0]
    print('###########################')
    print('Start scraping page', numPage)
    print('The url is', url)
    
    headers['User-Agent'] = random.choice(user_agents)        
    
    for num_connection_attempt in range(1,101):
        try:
            print('Number of connections attempted', num_connection_attempt)
            
            # This can be problematic as it will select the same proxies
            proxy = {'https': 'https://'+random.choice(proxies)}
            
            print('Proxy used:', proxy)
            # This is here because I cannot find a stable proxy;
            # proxy = {'https': 'https://176.196.225.54:1088'}

            response = requests.get(url, headers = headers, proxies = proxy, timeout=10.0)
            print('Response retrieved', response)
            html = response.content
            print('Connection established')
            break
        except (OSError, MaxRetryError, ProxyError, Timeout) as e:
            print(e)
            #print(e)
            if (num_connection_attempt == 100):
                output.close()
                sys.exit(0)
            continue
            
    soup = BeautifulSoup(html, 'lxml')    
    body = soup.find('body')
    table = body.find('span',attrs={'data-component-type': 's-search-results'})
    products = table.find_all('div',attrs={'data-component-type': 's-search-result'})
    if (products):
        print('Product list successfully pulled on page', numPage)
            
    # PROBLEM: The page pulled looks different from the page appears in Chrome
    
    for product in products:
        #DEBUG
        #print(product.attrs['data-index'])    
        product_info = product.find('div',{'class':'a-section a-spacing-medium'})
        
        img = product_info.find('img')
        img_link = img.attrs['src']
        name = product_info.find('h2').find('span').text
        
        rating_cell = product_info.find('div',{'class':'a-row a-size-small'})
        if rating_cell is None:
            rating = ' '
            num_rating = ' '
        else:
            rating_cell = rating_cell.find('span')
            if rating_cell is None:
                rating = ' '
                num_rating = ' '
            else:        
                num_rating_cell = rating_cell.find_next('span').find_next('span').find_next('span')
                rating = rating_cell.attrs['aria-label']
                num_rating = num_rating_cell.attrs['aria-label']
    
        price = product_info.find('span',{'class':'a-offscreen'})
        if price is None:
            price = ' '
        else: price = price.text
        
        list_info = [name,price,rating,num_rating,img_link]
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
    next_button = table.find('li',{'class':'a-last'})
    # Approach 1
    if next_button is not None:
               
        # There should be a way to automatically get href from next_button
        # The challenge is to eliminate tracking information Amazon puts in them        
        # href = next_button.find('a').attrs['href']
        href = '&page=' + str(numPage+1)
        next_url = head_href + product_href + href
        pages.append(next_url)
    
    print('Page scraped:',numPage,'\n')
    numPage = numPage+1
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






