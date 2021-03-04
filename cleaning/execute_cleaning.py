import os
import pandas as pd
import time

import data_prep
import freq_analysis
from features_extract import numeric_extract
from features_extract import price_extract
from features_extract import feature_extract
from features_extract import ID_extract
from features_extract import mfrID_extract
from features_extract import factorize
from features_extract import replace_blank
from list_flatten import list_flatten
from parameters_by_retailer import param_retailer as param

from rating_extract_newegg import rating_extract_newegg

######################### change these parameters ############################
path = 'C:\\Users\\roy79\\Desktop\\Research\\product-analysis'
working_dir = path + '\\cleaning'

retailer_name = 'newegg'

data_path = path+'\\raw_data\\'+retailer_name+'_hdphone.csv'
products = pd.read_csv(data_path)

# d.n change colnames and features_re
colnames = param[retailer_name]['colnames']
features_re = param[retailer_name]['features_re']
# used as arguments in factorize(), None by default
factorize_conn_col = param[retailer_name]['factorize_conn_col']
factorize_type_col = param[retailer_name]['factorize_type_col']


# extract integer/float (ID, price, etc.) from these columns
numeric_columns = [
    # For Walmart
#    colnames['COLNAME_RATING'],
#    colnames['COLNAME_NUM_RATING'], 
#    colnames['COLNAME_RETAILER_ID'],
    '_UPC_'
    ]
#'UPC']


# replace np.nan in these columns with 0
# if bhpv, then '' because it doesn't have a colname_about
feat_replace = ''
if (colnames['COLNAME_ABOUT'] != ''):
    feat_replace = ['_connection_', '_microphone_']


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
    # DEBUG
    #print(sum(products['name'] == np.nan))
    products = data_prep.remove_blank_row(products,colnames['COLNAME_TITLE'])
    # DEBUGs
    #print(sum(products['name'] == np.nan))

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
    
    # Extract price
    print('Extract price')
    price_extract(products,colnames['COLNAME_PRICE_CUR'], colnames['COLNAME_PRICE_ORIG'])
    
    # Extract numbers from select columns
    print('Extract numerics from columns')
    numeric_extract(products, numeric_columns)
    
    mfrID_extract(products, '_manufacturerID_')
    
    
    # Extract IDs
    if (colnames['COLNAME_MODEL'] != ''):
        print('Extract semi-numeric IDs')
        ID_extract(products, colnames['COLNAME_MODEL'])
    
    
    # This is for Newegg because its rating is embedded in unstructured text
    if (retailer_name == 'newegg'):
        print('Newegg specific cleanup functions')
        rating_extract_newegg(products,colnames['COLNAME_RATING'])
        products[colnames['COLNAME_NUM_RATING']] = products[colnames['COLNAME_NUM_RATING']]*(-1)
    
    
    # Categorize these columns
    print('Factorize columns')
    
    if (colnames['COLNAME_ABOUT'] != ''):
        factorize(products, 
                  mic_colname='_microphone_', 
                  noise_colname='_noise_', 
                  water_colname='_water_',
                  # This line is specific to walmart, change column names to fit your dataset / or comment out before run
                  wireless_colname=factorize_conn_col,
                  # This line is specific to walmart, change column names to fit your dataset / or comment out before run
                  type_colname=factorize_type_col)


    # Replace blank cells with 0 in these columns
    if (feat_replace != ''):
        print('Replace empty cells with 0 in select columns')
        replace_blank(products, feat_replace)

    print('Save cleaned csv to: ' + working_dir)
    products.to_csv(retailer_name+'_hdphone_cleaned_',index=False)

execute()
    
    # todo:
        # 
        # combine columns
    
    
    
    