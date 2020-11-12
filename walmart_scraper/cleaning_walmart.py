import json
import os
import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

os.chdir('C:\\Users\\roy79\\Desktop\\Research\\product-analysis\\walmart_scraper')

products = pd.read_csv('walmart_headphones_openRefine.csv')


string = products['about_text'][1]
string_sent = nltk.sent_tokenize(string)
string_word = nltk.word_tokenize(string)


# Discover pattern / common words in about with nltk
products['about_text_clean'] = products['about_text']
products['about_text_clean'] = products['about_text_clean'].str.lower()
products['about_text_clean'] = products['about_text_clean'].str.replace('^a-zA-Z#.',' ')

word_token = products['about_text_clean'].apply(lambda x: x.split())
word_token_stop = word_token.apply(lambda x: [w for w in x if w not in stopwords.words('english')])
word_token_unnest = sum(word_token_stop,[])
word_freq = nltk.FreqDist(word_token_unnest)
word_freq_df = pd.DataFrame({'word':list(word_freq.keys()),
                             'count':list(word_freq.values())})
word_freq_df = word_freq_df.sort_values('count',ascending=False)


# Create trigrams
trigrams = [list(nltk.trigrams(x.split())) for x in products['about_text_clean']]
trigrams_concat = []
for row in trigrams:
    tri = [' '.join(tuples) for tuples in row]
    trigrams_concat.append(tri)
trigrams_unnest = sum(trigrams_concat,[])
trigrams_freq = nltk.FreqDist(trigrams_unnest)

trigrams_freq_df = pd.DataFrame({'word':list(trigrams_freq.keys()),
                             'count':list(trigrams_freq.values())})
trigrams_freq_df = trigrams_freq_df.sort_values('count',ascending=False)


trigrams_freq_df[trigrams_freq_df['word'].str.contains('model')].head(50)


# words related to noise
word_freq_df[word_freq_df['word'].str.contains('noise')]
word_freq_df[word_freq_df['word'].str.contains('water')]
word_freq_df[word_freq_df['word'].str.contains('ipx')]
word_freq_df[word_freq_df['word'].str.contains('ear')].head(60)
word_freq_df[word_freq_df['word'].str.contains('type')].head(60)
word_freq_df[word_freq_df['word'].str.contains('oz')].head(60)

products[products['about_text_clean'].str.contains('upc')].loc[:,'about_text_clean']

# noise type
test_string = 'noise cancelling headphones'
test_string = 'noise reduction headphones'
test_string = 'sound isolation headphones'

noise = re.search('(noise|sound)(\-| )?(cancel|reduct|isolat)(\w+)', test_string)

# water resistant/proof == ipx4/ipx6
test_string = 'waterproof headphones'
test_string = 'water proof headphones'
test_string = 'water-resistant headphones'
test_string = 'ipx5'

water = re.search('water(\-| )?(proof|resist)', test_string)
if (water):
    print(water.group())
else:
    water = re.search('ipx[0-9]', test_string)
    if (water):
        print(water.group())

# microphone
test_string = 'microphone included'
test_string = 'mic included'
test_string = '3 mics'
mic = re.search('mic', test_string)

# type
test_string = 'on-ear'
test_string = 'over-the-ear'
test_string = 'on ear'
ear_type = re.search('(in|on|over)(-the)?(\-| )ear',test_string)


# connection: if both wireless and wired (detachable cable), then it's considered wireless
# some headphones say they are wired between left and right buds, so search for wireless first
test_string = 'bluetooth'
test_string = 'wireless'
test_string = 'bluetooth headphones and wireless charging case'
connection = re.search('bluetooth|wireless', test_string)

if (connection):
    print(connection.group())
else:
    print('wired')

# battery: this will get us the charging time; if charging time comes first in about, then battery life will not be found
# maybe only search for >= 3 hours; but would this stop us from getting 13 hours? (leading digit=1)
test_string = '8+ hours'
test_string = '8.5 hours'
test_string = 'charging time: 2 hours; battery life: 8 hours'
test_string = 'charging time: 2 hours; battery life: 8 hrs'

battery = re.findall('(\d+(\.\d+)?)+(\+)?( )?(hour|hours|hrs)',test_string)
battery_life = [i[0] for i in battery if int(i[0])>4]


# cord/cable length

# warrenty: no warrent in about; prob in a different section of the website
products[products['about_text_clean'].str.contains('warrent')].loc[:,'about_text_clean']

# weight
test_string = '8.23oz'
test_string = '8 oz'
test_string = '50g'
test_string = 'lightweight'
weight = re.search('(\d+(\.\d+)?)( )?(g|kg|oz|lb)', test_string)
if (weight):
    print(weight.group())
else:
    weight = re.search('(\w+)(weight)', test_string)
    if (weight):
        print(weight.group())

# driver type/unit size
test_string = 'battery life is 8 hours'
test_string = '8+ hours'
test_string = '8 hrs'

# impedance
test_string = '32 ohms'

re.search('(\d)( )?(ohms)', test_string)

# Frequency response/range
test_string = '20 hertz'
test_string = '20 kilohertz'

freq = re.search('(\d+)( )?(hertz|hz|kilohertz|khz)', test_string)

# Sensitivity
test_string = '100 decibels adjusted'
test_string = '100 db'
test_string = '22 db / 22 decibels adjusted'

sens = re.search('(\d+)( )?(decibels|decibel|db)( adjusted)?',test_string)


# UPC


# MODEL NUMBER


# brand: search in Name; do not consider brand as a feature; this is more or less irrelevant to the analysis

# =============================================================================
# features = ['brand',
# 'connection',
# 'type',
# 'battery',
# 'microphone',
# 'noise',
# 'water',
# 'cord',
# 'warranty',
# 'weight',
# 'driver',
# 'impedance',
# 'frequency response',
# 'sensitivity',
# 'UPC',
# 'model number',
# 'manufacturerID']
# =============================================================================


features = {'brand':'TODO: brand',
           'connection':'bluetooth|wireless',
            'type': '(in|on|over)(-the)?(\-| )ear',
            'battery':'(\d+(\.\d+)?)+(\+)?( )?(hour|hours|hrs)',
            'microphone':'mic',
            'noise': '(noise|sound)(\-| )?(cancel|reduct|isolat)(\w+)',
            'water': 'water(\-| )?(proof|resist)',
            'ipx':'ipx[0-9]',
            'cord':'TODO: cord',
            'warranty':'TODO: warranty',
            'weight':'(\d+(\.\d+)?)( )?(g|kg|oz|lb)',
            'driver':
            'impedance':
            'frequency response':
            'sensitivity':
            'UPC':
            'model number':
            'manufacturerID' 
    }

#we need a different way to search features like driver


for feat in features:
    if (feat == 'brand'):
        print('TODO: brand')
    elif (feat == 'connection'):
        connection = re.search('bluetooth|wireless', test_string, re.I)
        if (connection):
            print(connection.group())
        else:
            print('wired')
    elif (feat == 'type'):
        ear_type = re.search('(in|on|over)(-the)?(\-| )ear',test_string)
    elif (feat == 'battery'):
        battery = re.findall('(\d+(\.\d+)?)+(\+)?( )?(hour|hours|hrs)',test_string)
        battery_life = [i[0] for i in battery if int(i[0])>4]
    elif (feat == 'microphone'):
        mic = re.search('mic', test_string)
    elif (feat == 'noise'):
        noise = re.search('(noise|sound)(\-| )?(cancel|reduct|isolat)(\w+)', test_string)
    elif (feat == 'water'):
        water = re.search('water(\-| )?(proof|resist)', test_string)
        if (water):
            print(water.group())
        else:
            water = re.search('ipx[0-9]', test_string)
            if (water):
                print(water.group())                
    elif (feat == 'cord'):
        print('TODO: cord')
    elif (feat == 'warranty'):
        print('TODO: warranty')
    elif (feat == 'weight'):
        weight = re.search('(\d+(\.\d+)?)( )?(g|kg|oz|lb)', test_string)
        if (weight):
            print(weight.group())
        else:
            weight = re.search('(\w+)(weight)', test_string)
            if (weight):
                print(weight.group())
    elif (feat == 'driver'):
        print('TODO: driver')
    elif (feat == 'impedance'):
        imped = re.search('(\d)( )?(ohms)', test_string)
    elif (feat == 'frequency response'):
        freq = re.search('(\d+)( )?(hertz|hz|kilohertz|khz)', test_string)
    elif (feat == 'sensitivity'):
        sens = re.search('(\d+)( )?(decibels|decibel|db)( adjusted)?',test_string)
    elif (feat == 'UPC'):
        print('TODO: UPC')
    elif (feat == 'model number'):
        print('TODO: model number')
    elif (feat == 'manufacturerID'):
        print('TODO: manufacturerID')


# Flatten features
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





# join more than one datasets
num_pages = 6
products = []
for i in range(1,num_pages+1):
    file = 'laptop_page'+str(i)+'.json'
    print(file)
    with open(file,'rb') as fin:
        content = json.load(fin)
    print('page',i,'loaded successfully')
    products = products + (content['products']) 
    





with open('laptop.json', 'w') as fout:
    json.dump(products,fout,indent=1)