import os
import pandas as pd
import time

import data_prep
import freq_analysis
from features_extract import numeric_extract
from features_extract import feature_extract
from features_extract import mfrID_extract
from features_extract import factorize
from features_extract import replace_blank
from list_flatten import list_flatten
from parameters_by_retailer import param_retailer as param

######################### change these parameters ############################
path = 'C:\\Users\\roy79\\Desktop\\Research\\product-analysis'
# this is where the dataset is
data_path = path+'\\walmart_scraper\\'+'walmart_headphones_openRefine.csv'
working_dir = path + '\\cleaning'

#DEBUG
data_path = working_dir+'\\bestbuy_hdphone.csv'

retailer_name = 'bestbuy'

# d.n change colnames and features_re
colnames = param[retailer_name]['colnames']
features_re = param[retailer_name]['features_re']

### The parameters below can be determined by looking at the columns and variable types in the dataset
### However, some may not be obvious at first; and can be determined after we step through remove_used()
# set to None if not needed
# used as arguments in factorize()
factorize_conn_col_walmart = 'Wireless'
factorize_type_col_walmart = ['HeadphoneType','HeadphoneStyle','type']

factorize_conn_col_bestbuy = None
factorize_type_col_bestbuy = 'type'

factorize_conn_col = factorize_conn_col_bestbuy
factorize_type_col = factorize_type_col_bestbuy


# extract integer/float (ID, price, etc.) from these columns
numeric_columns = [colnames['COLNAME_NUM_RATING'], 
                  colnames['COLNAME_PRICE'],
                  #colnames['COLNAME_RETAILER_ID'],
                  'UPC']
# replace np.nan in these columns with 0
feat_replace = ['connection', 'microphone']


##############################################################################

# print most frequent words related to feature
# returns word frequency count for later use to avoid expensive frequency count
# ngram = 1 or 3
def word_freq_analysis(products, ngram, feature, word_freq_df=None):
    # Exploratory Analysis: 
    # find most frequently associated word for each feature
    # eg. features: 'noise'-> noise cancelling; noise reduction; ...
    # update features_re if necessary
    
    is_return = False
    
    if (word_freq_df is None):
        is_return = True
        if (ngram == 1):
            word_freq_df = freq_analysis.unigram_freq(products)
        if (ngram == 3):
            word_freq_df = freq_analysis.trigram_freq(products)
    
    most_freq = freq_analysis.most_freq_word_feat(word_freq_df,feature)
    print(most_freq)
    
    if (is_return == True):
        return word_freq_df


def execute():
    
    # set working directory
    os.chdir(working_dir)
    products = pd.read_csv(data_path)
    print('Successfully loaded dataset')
    
    # run next line to print all colnames after loading the dataset
    # products.columns
    
    # This helps remove empty rows that accidentally gets scraped
    products = data_prep.remove_blank_row(products,colnames['COLNAME_TITLE'])
    
    
    # clean the about / description text and put them in column: 'about_text_clean'
    if (colnames['COLNAME_ABOUT'] != ''):
        print('Start about/description preparation')
        data_prep.about_prep(products,colnames['COLNAME_ABOUT'])
        
        
    # =============================================================================
    #     # This is useful for determining what keywords to search for each feature
    #     # exploratory analysis
    #     print('Start Word Frequency Analysis')
    #     word_freq = word_freq_analysis(products, 1, 'noise')
    #     trigram_freq = word_freq_analysis(products, 3, 'frequency')
    #     word_freq_analysis(products, 3, 'noise', trigram_freq)
    # =============================================================================
        
        # Extract features from about/description
        print('Start Feature Extraction')
        feat_ext_df = feature_extract(products, features_re)
        products = pd.concat([products, feat_ext_df], axis=1)
    
    # Flatten any lists
    if (colnames['COLNAME_FEAT_LABELS'] != ''):
        print('Start List Flattening')
        data_prep.list_clean(products, 
                             colnames['COLNAME_FEAT_LABELS'], 
                             colnames['COLNAME_FEAT_VALUES'])
        flattened_feat = list_flatten(products)
        
        # Combine the extracted features and the original dataset
        products = pd.concat([products, flattened_feat], axis=1)    
    
    # Remove used products
    print('Remove used products')
    products = data_prep.remove_used(products, colnames['COLNAME_TITLE'])
    
    # Extract numbers from select columns
    print('Extract numerics from columns')
    numeric_extract(products, numeric_columns)
    
    mfrID_extract(products, 'manufacturerID')
    
    # Categorize these columns
    print('Factorize columns')
    factorize(products, 
              mic_colname='microphone', 
              noise_colname='noise', 
              water_colname='water',
              # This line is specific to walmart, change column names to fit your dataset / or comment out before run
              wireless_colname=factorize_conn_col,
              # This line is specific to walmart, change column names to fit your dataset / or comment out before run
              type_colname=factorize_type_col)


    # Replace blank cells with 0 in these columns
    print('Replace empty cells with 0 in select columns')
    replace_blank(products, feat_replace)

    print('Save cleaned csv to: ' + working_dir)
    products.to_csv('products_cleaned'+time.strftime("%Y%m%d-%H%M%S")+'.csv')

execute()
    
    # todo:
        # 
        # combine columns
    
    
    
    