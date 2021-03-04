import pandas as pd
import numpy as np
import re

# Clean unstructured text
def about_prep(products, col_about):
    
#    col_about = colnames['COLNAME_ABOUT']
    if (col_about == ''):
        return
    if (type(col_about) == list):
        products['about_text_clean'] = products[col_about[0]].astype(str)
        for i in range(1,len(col_about)-1):
            if (i is not np.nan):
                products['about_text_clean'] = products['about_text_clean'] + ' ' + products[col_about[i]].astype(str)
                
    else:
        products['about_text_clean'] = products[col_about].astype(str)
    
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
    is_used = products[colname_title].str.contains(r'refurbish|used', flags=re.I, na=False)
    return products[-is_used]