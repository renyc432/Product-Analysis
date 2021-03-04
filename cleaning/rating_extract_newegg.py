import pandas as pd
import numpy as np
import re

def rating_extract_newegg(products, col_rating):
    col_rating = 'table_reviews_text'
    products[col_rating] = products[col_rating].str.replace(',', '')
    
    rating_ext = [re.search('\d+( out of 5 eggs)', string, re.I).group() 
                  if (type(string) == str and re.search('\d+( out of 5 eggs)', string, re.I) is not None) else np.nan
                  for string in products[col_rating]]


    rating_ext_int = [int(rate[0]) if type(rate) == str else np.nan for rate in rating_ext]

    products['_rating_'] = rating_ext_int
    print('Created column \'_rating_\'; refer to this column for rating feature')