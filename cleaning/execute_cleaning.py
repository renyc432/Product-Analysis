import os
import pandas as pd

import text_prep
from features_extract import feature_extraction
from list_flatten import list_flatten


path = 'C:\\Users\\roy79\\Desktop\\Research\\product-analysis'
# Colnames of about / description
COLNAME_ABOUT = ['about_text','about_details']

# Colnames of features in ['wireless', 'type'] format
COLNAME_LABELS = 'feat_labels'
COLNAME_VALUES = 'feat_values'

features_re = {'brand':'TODO: brand',
            # connection: if both wireless and wired (detachable cable), then it's considered wireless
           'connection':'bluetooth|wireless',
            'type': '(in|on|over)(-the)?(\-| )ear',
            'battery':'(\d+(\.\d+)?)+(\+)?( )?(hour|hours|hrs)',
            'microphone':'mic',
            'noise': '(noise|sound)(\-| )?(cancel|reduct|isolat)(\w+)',
            'water': 'water(\-| )?(proof|resist)',
#            'ipx':'ipx[0-9]',
#            'cord':'TODO: cord',
            'warranty':'TODO: warranty',
            'weight':'(\d+(\.\d+)?)( )?(g|kg|oz|lb)',
            'driver': 'TODO: driver',
            'impedance': '(\d)( )?(ohms)',
            'frequency response': '(\d+)( )?(hertz|hz|kilohertz|khz)',
            'sensitivity': '(\d+)( )?(decibels|decibel|db)( adjusted)?',
            'UPC': 'TODO: UPC',
            'model number': 'TODO: model number',
            'manufacturerID': 'TODO: manufacturerID'
    }



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
            word_freq_df = text_prep.unigram_freq(products)
        if (ngram == 3):
            word_freq_df = text_prep.trigram_freq(products)
            
    most_freq = text_prep.most_freq_word_feat(word_freq_df,feature)
    print(most_freq)
    
    if (is_return == True):
        return word_freq_df


def execute():
    os.chdir(path+'\\cleaning')
    products = pd.read_csv(path+'\\walmart_scraper\\'+'walmart_headphones_openRefine.csv')
    
    # clean the about / description and put them in column: about_text_clean
    text_prep.about_prep(products,COLNAME_ABOUT)
    
    # exploratory analysis
    word_freq = word_freq_analysis(products, 1, 'noise')
    trigram_freq = word_freq_analysis(products, 3, 'frequency')
    word_freq_analysis(products, 3, 'noise', trigram_freq)
    
    # Extract features from about/description
    feat_ext_df = feature_extraction(products, features_re)
    
    # Optional flatten the list
    if (COLNAME_LABELS != ''):
        text_prep.list_clean(products)
        flattened_feat = list_flatten(products)
        products = pd.concat([products, feat_ext_df, flattened_feat], axis=1)
    
    
    products = pd.concat([products, feat_ext_df], axis=1)


    
    # change text to numbers
    # combine strings like noise-cancellation and noise cancelling
    # remove unnecessary strings in all columns eg. 'ratings'
    
    
    
    
    
    
    
    
    
    