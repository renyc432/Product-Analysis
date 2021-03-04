import numpy as np
import pandas as pd
import re
from features_extract import numeric_extract
from execute_cleaning import path
from execute_cleaning import working_dir
#from execute_cleaning import retailer_name
import time

# Only works for headphone
def col_merge(type_1, type_2):
    if (type_1 is np.nan and type_2 is np.nan):
        return np.nan
    if (type_1 is np.nan):
        return type_2
    if(type_2 is np.nan):
        return type_1
    return type_1

def hdphones_form_factor_amazon(data_am):
    
    # TODO: Code redundancy
    colname = 'headphones_form_factor'
    
    is_on = data_am[colname].str.contains(r'on', flags = re.I).replace(np.nan,False)
    is_in = data_am[colname].str.contains(r'in', flags = re.I).replace(np.nan,False)
    is_over = data_am[colname].str.contains(r'over', flags = re.I).replace(np.nan,False)
    
    data_am.loc[is_on,colname] = 'on'
    data_am.loc[is_in,colname] = 'in'
    data_am.loc[is_over,colname] = 'over'
    
    is_earbud = data_am[colname].str.contains(r'earbud', flags = re.I).replace(np.nan,False)
    is_fold = data_am[colname].str.contains(r'fold', flags = re.I).replace(np.nan,False)
    is_back = data_am[colname].str.contains(r'fold', flags = re.I).replace(np.nan,False)
    
    data_am.loc[is_earbud,colname] = 'in'
    data_am.loc[is_fold,colname] = 'over'
    data_am.loc[is_back,colname] = 'over'

    is_not_zero = pd.Series([bool(i+j+k+l+m+n) 
                             for i,j,k,l,m,n
                             in zip(is_on,is_in,is_over,is_earbud,is_fold,is_back)], index = data.index)

    data.loc[-is_not_zero,colname] = np.nan


def connection_amazon(data_am):
    
    colname = 'connection'
    
    is_wired = data_am[colname].str.contains(r'wired', flags = re.I).replace(np.nan,False)
    is_bluetooth = data_am[colname].str.contains(r'bluetooth', flags = re.I).replace(np.nan,False)
    is_wireless = data_am[colname].str.contains(r'wireless', flags = re.I).replace(np.nan,False)
    
    data_am.loc[is_wired,colname] = 0
    data_am.loc[is_bluetooth,colname] = 1
    data_am.loc[is_wireless,colname] = 1

    is_not_zero = pd.Series([bool(i+j+k) 
                             for i,j,k
                             in zip(is_wired,is_bluetooth,is_wireless)], index = data.index)

    data.loc[-is_not_zero,colname] = np.nan
    

def combine_amazon(data_am):
    
    print('Amazon: combine features spread out in multiple columns')
    # Combine: 'headphones_form_factor' and '_type_'
    hdphones_form_factor_amazon(data_am)
    data_am['_type_'] = [col_merge(t_1,t_2) 
                         for t_1, t_2 in zip(data_am['headphones_form_factor'], 
                                             data_am['_type_'])]
    print('Feature \'type\' combined. Find in \'_type_\'')
    data_am.drop('headphones_form_factor', axis=1, inplace=True)
    
    # Combine: 'connection' and '_connection_'
    connection_amazon(data_am)
    data_am['_connection_'] = [col_merge(t_1,t_2) 
                         for t_1, t_2 in zip(data_am['connection'], 
                                             data_am['_connection_'])]
    print('Feature \'connection\' combined. Find in \'_connection_\'')
    data_am.drop('connection', axis=1, inplace=True)
    

def type_newegg(data_ne):
    
    colname = 'type'
    
    is_on = data_ne[colname].str.contains(r'on', flags = re.I).replace(np.nan,False)
    is_in = data_ne[colname].str.contains(r'in', flags = re.I).replace(np.nan,False)
    is_over = data_ne[colname].str.contains(r'over', flags = re.I).replace(np.nan,False)
    
    data_ne.loc[is_on,colname] = 'on'
    data_ne.loc[is_in,colname] = 'in'
    data_ne.loc[is_over,colname] = 'over'
    
    is_earbud = data_ne[colname].str.contains(r'earbud', flags = re.I).replace(np.nan,False)
    is_headset = data_ne[colname].str.contains(r'headset', flags = re.I).replace(np.nan,False)
    is_DJ = data_ne[colname].str.contains(r'dj', flags = re.I).replace(np.nan,False)
    
    data_ne.loc[is_earbud,colname] = 'in'
    data_ne.loc[is_headset,colname] = 'over'
    data_ne.loc[is_DJ,colname] = 'over'

    is_not_zero = pd.Series([bool(i+j+k+l+m+n) 
                             for i,j,k,l,m,n
                             in zip(is_on,is_in,is_over,is_earbud,is_headset,is_DJ)], index = data.index)

    data.loc[-is_not_zero,colname] = np.nan
    

def wireless_type_newegg(data_ne):
    data_ne['wireless_type'] = data_ne['wireless_type'].replace('No',0)
    data_ne['wireless_type'] = [0 if w == np.nan else 1 
                                for w in data_ne['wireless_type']]
    

def combine_newegg(data_ne):
    print('Newegg: combine features spread out in multiple columns')

    # Combine: 'type' and '_type_'
    type_newegg(data_ne)
    data_ne['_type_'] = [col_merge(t_1,t_2) 
                         for t_1, t_2 in zip(data_ne['type'], 
                                             data_ne['_type_'])]
    print('Feature \'type\' combined. Find in \'_type_\'')

    # Combine: 'wireless_type' and '_connection_'
    wireless_type_newegg(data_ne)
    data_ne['_connection_'] = [col_merge(t_1,t_2) 
                               for t_1, t_2 in zip(data_ne['wireless_type'], 
                                                   data_ne['_connection_'])]
    print('Feature \'connection\' combined. Find in \'_connection_\'')

    # Combine: 'battery_life' and '_battery_'
    #numeric_extract(data_ne, 'battery_life')
    
# =============================================================================
#     data_ne['battery_life'] = [float(re.search('(\d+(.\d+)?)', ID, re.I).group())
#                                if type(ID) == str else np.nan 
#                                for ID in data_ne['battery_life']]
#     
#     
#     data_ne['_battery_'] = [col_merge(t_1,t_2) 
#                             for t_1, t_2 in zip(data_ne['battery_life'], 
#                                                 data_ne['_battery_'])]
#     print('Feature \'battery\' combined. Find in \'_battery_\'')
# =============================================================================

    data_ne.drop(['type','wireless_type','battery_life'], axis=1, inplace=True)

    
def combine_bestbuy(data_bb):
    print('Bestbuy: nothing to combine')
    

def combine_walmart(data_wm):
    print('Walmart: nothing to combine')

    
def col_combine(data, retailer):
    if (retailer == 'amazon'):
        combine_amazon(data)
    if (retailer == 'bestbuy'):
        combine_bestbuy(data)
    if (retailer == 'newegg'):
        combine_newegg(data)
    if (retailer == 'walmart'):
        combine_walmart(data)
    
    data.to_csv(retailer_name+'_hdphone_cleaned_col-combined_'+time.strftime("%Y%m%d-%H%M%S")+'.csv')
    
    


filename = 'amazon_hdphone_cleaned.csv'

data_path =  path + '\\clean_data\\'+filename

data = pd.read_csv(data_path)

retailer_name = 'amazon'

col_combine(data, retailer_name)
    
#a = data['type'].value_counts()
    
    
# =============================================================================
# test = '4-6 Hours'
# re.search('(\d+(.\d+)?)', test, re.I)
# =============================================================================
    
    
    