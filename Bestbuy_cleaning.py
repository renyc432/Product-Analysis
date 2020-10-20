# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 00:22:05 2020

@author: rs
"""

import json
import os


os.chdir('C:\\Users\\rs\\Desktop\\MScA\\Quarter 1\\MSCA 31012 4\\Final Project\\Bestbuy')


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