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
    products['about_text_clean'] = [re.sub('[^a-zA-Z#.]', ' ', prod) for prod in products['about_text_clean']]
    
# Calculate word (unigram) frequency
def unigram_freq(products):
    word_token = products['about_text_clean'].apply(lambda x: x.split())
    word_token_stop = word_token.apply(lambda x: [w for w in x if w not in stopwords.words('english')])
    word_token_unnest = sum(word_token_stop,[])
    word_freq = nltk.FreqDist(word_token_unnest)
    word_freq_df = pd.DataFrame({'word':list(word_freq.keys()),
                                 'count':list(word_freq.values())})
    return word_freq_df

# Calculate trigram frequency
def trigram_freq(products):
    trigrams = [list(nltk.trigrams(x.split())) for x in products['about_text_clean']]
    trigrams_concat = []
    for row in trigrams:
        tri = [' '.join(tuples) for tuples in row]
        trigrams_concat.append(tri)
    trigrams_unnest = sum(trigrams_concat,[])
    trigrams_freq = nltk.FreqDist(trigrams_unnest)
    trigrams_freq_df = pd.DataFrame({'word':list(trigrams_freq.keys()),
                                 'count':list(trigrams_freq.values())})
    return trigrams_freq_df

# print top 50 most common unigram (word)
def most_freq_word_feat(freq_dist, feature):
    #word_freq_df = freq_dist.sort_values(feature,ascending=False)
    freq = freq_dist[freq_dist['word'].str.contains(feature)].head(50)
    print(freq.sort_values('count',ascending=False))


#remove '' and []
def clean_list_helper(string):
    if (string is np.nan):
        return ''
    return re.sub('[\[\]\' ]', '', string)
    
def list_clean(products):
    products['feat_labels_clean'] = [clean_list_helper(feat_row) for feat_row in products['feat_labels']]
    products['feat_values_clean'] = [clean_list_helper(feat_row) for feat_row in products['feat_values']]