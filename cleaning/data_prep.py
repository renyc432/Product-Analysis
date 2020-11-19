import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords

# Clean unstructured text
def about_prep(products, colnames):
    if (colnames == ''):
        return
    if (type(colnames) == list):
        products['about_text_clean'] = products[colnames[0]]
        for i in range(1,len(colnames)-1):
            if (i is not np.nan):
                products['about_text_clean'] = products['about_text_clean'] + ' ' + products[colnames[i]]
                
    else:
        products['about_text_clean'] = products[colnames]
    
    products['about_text_clean'] = products['about_text_clean'].str.lower()    
    products['about_text_clean'] = [re.sub('[^a-zA-Z0-9.]', ' ', prod) 
                                    if prod is not np.nan else '' for prod in products['about_text_clean']]


#remove '' and []
def clean_list_helper(string):
    if (string is np.nan):
        return ''
    return re.sub('[\[\]\' ]', '', string)
    
def list_clean(products, labels, values):
    products['feat_labels_clean'] = [clean_list_helper(feat_row) for feat_row in products[labels]]
    products['feat_values_clean'] = [clean_list_helper(feat_row) for feat_row in products[values]]
    

def remove_blank_row(products, colname_title):
    is_blank = pd.isna(products[colname_title])
    return products[-is_blank]
    
def remove_used(products, colname_title):
    is_used = products[colname_title].str.contains(r'refurbish|used', flags=re.I)
    return products[-is_used]