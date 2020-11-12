from bs4 import BeautifulSoup
import requests
import sys
import time
import random
import scraper_setting as st

def listing_url_request(url, headers, output, num_page_listing):
    for num_request_attempt in range(1,101):
        try:   
            response = requests.get(url,headers=headers)
            html = response.content
            
# =============================================================================
#             # use a separate except to catch sys.exit()
#             if ('Forbidden' in str(html)):
#                 output.close()
#                 print('You have reached the end of the listing pages. This category has been crawled. The program will terminate now.')
#                 sys.exit(0)
# =============================================================================
                
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
        
        
def product_url_request(prod_url, output, num_page_listing):
    for num_connection_attempt in range(1,101):
        try:
            #print('Number of connections attempted', num_connection_attempt)
            proxy = None
            if (num_connection_attempt > 1):
                # This can be problematic as it will select the same proxies
                proxy = {'https': 'https://'+random.choice(st.proxies)}
            prod_response = requests.get(prod_url, headers=st.headers, proxies=proxy, Timeout=10.0)
            prod_html = prod_response.content
            prod_soup = BeautifulSoup(prod_html, 'lxml')
            if (prod_soup.find(text='CAPTCHA')):
                raise Exception('CAPTCHA error, try a different proxy')            
            break
        except KeyboardInterrupt:
            output.close()
            sys.exit('Keyboard interrupt')
        except:
            if (num_connection_attempt == 1):
                print('##################################################')
                print('Captcha error when requesting a product, try a proxy.')
            if (num_connection_attempt == 100):
                print('Product is skipped at', prod_url)
                print('Sleep for 5 minutes')
                time.sleep(300)
                return prod_url
            continue       
        
    return prod_soup