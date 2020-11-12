from selenium import webdriver


driver_add = 'C:\\Users\\roy79\\Desktop\\Research\\product-analysis\\walmart_scraper\\chromedriver.exe'

def sel_get_url(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    driver = webdriver.Chrome(driver_add, options=options)
    driver.get(url)
    html = driver.page_source
    return html

url = 'https://www.walmart.com/ip/Beats-Flex-All-Day-Wireless-Earphones-Beats-Black/696881930'

html = sel_get_url(url)

