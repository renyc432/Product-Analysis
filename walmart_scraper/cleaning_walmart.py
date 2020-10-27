import json
import os
import pandas as pd


os.chdir('C:\\Users\\roy79\\Desktop\\Research\\product-analysis\\walmart_scraper')

products = pd.read_csv('walmart_headphones.csv')
num_pages = 6
products = []
for i in range(1,num_pages+1):
    file = 'laptop_page'+str(i)+'.json'
    print(file)
    with open(file,'rb') as fin:
        content = json.load(fin)
    print('page',i,'loaded successfully')
    products = products + (content['products']) 
    
    
# excluding features: frequentlyPurchasedWith, categoryPath, image, mobileUrl, 
#                     onlineAvailability, onlineAvailabiliyText, relatedProducts, includedItemList
features_del = ['frequentlyPurchasedWith',
                'categoryPath',
                'image',
                'mobileUrl',
                'onlineAvailability', 
                'onlineAvailabiliyText', 
                'relatedProduct',
                'includedItemList',
                'details',
                'features']

for product in products:
    
    # Flatten details
    for detail in product['details']:
        name = detail['name']
        values = ', '.join(detail['values'])
        product[name] = values
    
    # Flatten features
    features = ''
    for feature in product['features']:
        features = features + ', ' + feature['feature']
    product['features'] = features
    
    
    # Delete unnecessary features
    for i in features_del:
        product.pop(i,None)    



with open('laptop.json', 'w') as fout:
    json.dump(products,fout,indent=1)