import os
import pandas as pd
import time
import data_prep
import freq_analysis
from features_extract import ID_extract
from features_extract import feature_extraction
from features_extract import remove_decorative
from features_extract import factorize
from features_extract import replace_blank

from list_flatten import list_flatten
import re

######################### change these parameters ############################
path = 'C:\\Users\\roy79\\Desktop\\Research\\product-analysis'
# this is where the dataset is
data_path = path+'\\walmart_scraper\\'+'walmart_headphones_openRefine.csv'
working_dir = path + '\\cleaning'


colnames = {
    # colname: name of product
    'COLNAME_TITLE': 'name',
    # colname: retailer ID
    'COLNAME_RETAILER_ID': 'wm_ID',
    # colname: rating
    'COLNAME_RATING': 'rating',
    # colname: number of ratings
    'COLNAME_NUM_RATING': 'num_of_rating',
    # colname: price
    'COLNAME_PRICE': 'price',
    # Colnames of about / description
    'COLNAME_ABOUT': ['about_text','about_details'],
    # Colnames of features in ['wireless', 'type'] format
    'COLNAME_FEAT_LABELS': 'feat_labels',
    'COLNAME_FEAT_VALUES': 'feat_values'
    }

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
    
    
    # clean the about / description text and put them in column: 'about_text_clean'
    print('Start data preparation')
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
    feat_ext_df = feature_extraction(products)
    
    # Optional flatten the list
    if (colnames['COLNAME_FEAT_LABELS'] != ''):
        print('Start List Flattening')
        data_prep.list_clean(products, 
                             colnames['COLNAME_FEAT_LABELS'], 
                             colnames['COLNAME_FEAT_VALUES'])
        flattened_feat = list_flatten(products)
        
        # Combine the extracted features and the original dataset
        products = pd.concat([products, 
                              feat_ext_df, 
                              flattened_feat], axis=1)
    else:
        # Combine the extracted features and the original dataset
        products = pd.concat([products, feat_ext_df], axis=1)
    
    products = data_prep.remove_used(products)

    # Remove deocrative strings
    remove_decorative(products,
                      num_rating=colnames['COLNAME_NUM_RATING'], 
                      price=colnames['COLNAME_PRICE'])
    
    # Extract numbers from select columns
    ID_columns = [colnames['COLNAME_RETAILER_ID'],
                  'UPC',
                  'manufacturerID']
    ID_extract(products, ID_columns)
    
    # Categorize these columns
    factorize(products, 
              mic_colname='microphone', 
              noise_colname='noise', 
              water_colname='water',
              # This line is specific to walmart, change column names to fit your dataset / or comment out before run
              wireless_colname='Wireless',
              # This line is specific to walmart, change column names to fit your dataset / or comment out before run
              type_colname=['HeadphoneType','HeadphoneStyle','type'])


    # Replace blank cells with 0 in these columns
    feat_replace = ['connection', 'microphone']
    replace_blank(products, feat_replace)


    products.to_csv('products_cleaned'+time.strftime("%Y%m%d-%H%M%S")+'.csv')

execute()
    
    # todo:
        # feature extraction finish: brand not done
        # combine columns
    
    
    
    
    
    
    