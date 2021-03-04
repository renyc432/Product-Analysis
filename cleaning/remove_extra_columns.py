import pandas as pd
import time
from execute_cleaning import working_dir



# customize columns to remove after cleaning the data
col_remove_walmart = ['about_text',
                            'about_details',
                            'about_text_clean',
                            'feat_labels',
                            'feat_values',
                            'feat_labels_clean',
                            'feat_values_clean',
                            'RecommendedUse',
                            'CompatibleDevices',
                            'WirelessTechnology']

col_remove_bestbuy = ['about_text',
                            'about_details',
                            'about_text_clean',
                            'feat_labels',
                            'feat_values',
                            'feat_labels_clean',
                            'feat_values_clean',
                            'RecommendedUse',
                            'CompatibleDevices',
                            'WirelessTechnology']

col_remove = col_remove_walmart


# Identify columns to be removed
# Ideas: remove columns with three words or more except for colnames['COLNAME_TITLE']



def remove_columns(products, colnames):
    products.drop(colnames, inplace=True, axis=1)


def col_cleaning():
    products = pd.read_csv(working_dir+'\\products_cleaned.csv')

    remove_columns(products, col_remove)
    #combine_columns(products)
    
    products.to_csv('products_cleaned_colremoved'+time.strftime("%Y%m%d-%H%M%S")+'.csv')



# =============================================================================
# # after cleaning, there may be more than one column answering the same questions extracted from different places
# # for example, in walmart, 'HeadphoneType', 'HeadphoneStyle', 'type' all indicates whether a headphone is in-ear/on-ear/over-ear
# 
# 
# colnames = ['HeadphoneType', 'HeadphoneStyle', 'type']
# 
# # specify colnames and col_type
# # col_type is needed because different types have different merge rules
# # col_type values: type, connection
# def combine_columns(products, colnames, col_type):
#     
#     if (col_type == 'type'):
#         
#     
#     if (col_type == 'connection'):
#         for prod in products:
#             is_wireless = 1
#             for col in colnames:
# =============================================================================