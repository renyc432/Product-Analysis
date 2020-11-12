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

# change this to the category (laptops, headphones, etc.) of your choice
category_hrefs = ['/browse/headphones/headphones/3944_133251_1095191_4480?']

start_page = 'page=1'
