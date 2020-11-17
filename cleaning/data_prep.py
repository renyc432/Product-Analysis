import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords

# Clean unstructured text
def about_prep(products, colnames):
    colnames = ['about_text','about_details']
    if (len(colnames) > 1):
        products['about_text_clean'] = products[colnames[0]]
        for i in range(1,len(colnames)-1):
            products['about_text_clean'] = products['about_text_clean'] + ' ' + products[colnames[i]]
    
    products['about_text_clean'] = products[colnames]
    
    products['about_text_clean'] = products['about_text_clean'].str.lower()    
    products['about_text_clean'] = [re.sub('[^a-zA-Z0-9.]', ' ', prod) for prod in products['about_text_clean']]


#remove '' and []
def clean_list_helper(string):
    if (string is np.nan):
        return ''
    return re.sub('[\[\]\' ]', '', string)
    
def list_clean(products, labels, values):
    products['feat_labels_clean'] = [clean_list_helper(feat_row) for feat_row in products[labels]]
    products['feat_values_clean'] = [clean_list_helper(feat_row) for feat_row in products[values]]
    
    
    
def remove_used(products):
    is_used = products['name'].str.contains(r'refurbish|used', flags=re.I)
    return (products[-is_used])    