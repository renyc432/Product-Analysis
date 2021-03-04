import numpy as np
import pandas as pd
import re


test = '5'
re.search('(\d+(.\d+)?)', test, re.I)
float(1)

#test = 'manufacturerID: 3212-da_wd'
#re.search('(manufacturer|mfr|model)?(_|\s)?(number|#|ID|model)?( is)?(\s)?(:)?(\s+)?[\w\-+]+',test)

# helper: replace cells with 0 in these columns
def replace_blank(products, feat_colnames):
    for feat in feat_colnames:
        products[feat] = products[feat].replace(np.nan, 0)


# extracts numbers from columns;
# there must be only one number in the cell; 
# if more than one is present, the first number must be the target number
def numeric_extract(products, col_num):
    if (type(col_num) == list):
        for col in col_num:
            if (products[col].dtype != 'float64'):
                products[col] = products[col].str.replace(',','')
                products[col] = [float(re.search('(\d+(.\d+)?)', ID, re.I).group())
                                 if (type(ID) == str and 'cart' not in ID) 
                                 else np.nan for ID in products[col]]
    else:
        products[col_num] = products[col].str.replace(',','')
        if (products[col_num].dtype != 'float64'):
            products[col_num] = [float(re.search('(\d+(.\d+))', ID, re.I).group())
                                          if (type(ID) == str and 'cart' not in ID) 
                                          else np.nan for ID in products[col_num]]


# price extractor
def price_compare(price_cur, price_orig):
    if (price_cur is np.nan):
        return np.nan
    if (price_orig is np.nan):
        return price_cur
    if (price_cur <= price_orig):
        return price_orig
    return price_cur

def price_extract(products, col_price_cur, col_price_orig = None):
    
    products[col_price_cur] = products[col_price_cur].str.replace(',','')
    if (col_price_orig is None or col_price_orig == ''):
        products[col_price_cur] = [float(re.search('(\d+(.\d+)?)', p, re.I).group())
                                 if (type(p) == str and 'cart' not in p) else np.nan 
                                 for p in products[col_price_cur]]
        return
    
    products[col_price_orig] = products[col_price_orig].str.replace(',','')
    
    products[col_price_cur] = [float(re.search('(\d+(.\d+)?)', p, re.I).group())
                         if (type(p) == str and 'cart' not in p and '$' in p) else np.nan 
                         for p in products[col_price_cur]]
    
    products[col_price_orig] = [float(re.search('(\d+(.\d+)?)', p, re.I).group())
                         if (type(p) == str and 'cart' not in p and '$' in p) else np.nan 
                         for p in products[col_price_orig]]
    
    products['_price_'] = [price_compare(p_c,p_o) 
                           for p_c, p_o in zip(products[col_price_cur], products[col_price_orig])]
    print('Created column \'_price_\'; refer to this column for price feature')


# extracts the last element of the string
def mfrID_extract(products, colname_mfrID):
    products[colname_mfrID] = [ID.split()[-1] 
                               if type(ID) == str else np.nan for ID in products[colname_mfrID]]
    print('Created column \'_manufacturerID_\'. Not a necessarily useful column, delete if doesn\'t make sense')


# Extract model: this extracts everything after the first word
# eg: 'Model: FR37-A Marshmallow' -> 'FR37-A Marshmallow'
# eg: 'model# FR37-A Marshmallow' -> 'FR37-A Marshmallow'
def ID_extract(products, col_ID = None):
    
    if (col_ID != '' and col_ID is not None):
        new_colname = '_'+col_ID+'_'
        products[new_colname] = [ID.split(' ', maxsplit=1)[1] 
                               if (type(ID) == str) else np.nan
                               for ID in products[col_ID]]
        print('Created column \'', new_colname,'\'; refer to this column for the features')




def feat_ext_helper (features_re, feat, product_desp):
    
    # battery: if battery_life < 5, then that is likely charging time
    if (feat == '_battery_'):
        battery = re.findall(features_re['_battery_'], product_desp, re.I)    
        if (battery):
            battery_life = [i[0] for i in battery if float(i[0])>5]
            if (battery_life):           
                return max(battery_life)
        return np.nan
    
    if (feat == '_weight_'):
        weight = re.search(features_re['_weight_'], product_desp, re.I)
        if (weight):
            return weight.group()
        weight = re.search('(\w+)(weight)', product_desp, re.I)
        if (weight):
            return weight.group()
        return np.nan
       
    if (feat == '_water_'):
        water = re.search(features_re['_water_'], product_desp, re.I)
        if (water):
            return water.group()
        water = re.search('ipx[0-9]', product_desp, re.I)
        if (water):
            water_text = water.group()
            if (int(water_text[3]) >= 5):
                return 'water proof'
            return 'water resist'
        return np.nan
    
    if (feat == '_connection_'):
        connection = re.search(features_re['_connection_'], product_desp, re.I)
        if (connection):
            return 1
        return 0
    
    text = re.search(features_re[feat], product_desp, re.I)
    if (text):
        return text.group()
    return np.nan


def feature_extract (products, features_re):
    feat_ext_nested_list = []
    for product_description in products['about_text_clean']:
        feat_ext_row = [feat_ext_helper(features_re, feat, product_description) for feat in features_re.keys()]
        feat_ext_nested_list.append(feat_ext_row)    
    feat_ext_df = pd.DataFrame(feat_ext_nested_list, columns = list(features_re.keys()))
    
    feat_ext_df['_connection_'] = feat_ext_df['_connection_'].replace('bluetooth','wireless')
    return feat_ext_df

    
    

# factorize: turns column values into categories
# connection: wireless/bluetooth = 1
# type: keep as it is
# microphone: mic = 1
# noise: reduct ; cancel; isolate
# water: water proof ; water resist
# weight: ???
# Wireless: wired, nan = N; others = Y

# TODO: DUPLICATE CODE
def type_fact_helper(products, type_in):
    is_on = products[type_in].str.contains(r'on', flags = re.I).replace(np.nan,False)
    is_in = products[type_in].str.contains(r'in', flags = re.I).replace(np.nan,False)
    is_over = products[type_in].str.contains(r'over', flags = re.I).replace(np.nan,False)
    is_not_zero = pd.Series([bool(i+j+k) for i,j,k in zip(is_on,is_in,is_over)], index = products.index)
    
    products.loc[is_on,type_in] = 'on'
    products.loc[is_in,type_in] = 'in'
    products.loc[is_over,type_in] = 'over'
    products.loc[-is_not_zero,type_in] = np.nan

def noise_fact_helper(products, noise_in):
    is_reduct = products[noise_in].str.contains(r'reduct', flags = re.I).replace(np.nan,False)
    is_cancel = products[noise_in].str.contains(r'cancel', flags = re.I).replace(np.nan,False)
    is_isolate = products[noise_in].str.contains(r'isolat', flags = re.I).replace(np.nan,False)
    products.loc[is_reduct,noise_in] = 'reduct'
    products.loc[is_cancel,noise_in] = 'cancel'
    products.loc[is_isolate,noise_in] = 'isolate'

def water_fact_helper(products, water_in):
    is_proof = products[water_in].str.contains(r'proof', flags = re.I).replace(np.nan,False)
    is_resist = products[water_in].str.contains(r'resist', flags = re.I).replace(np.nan,False)
    products.loc[is_proof,water_in] = 'proof'
    products.loc[is_resist,water_in] = 'resist'

def factorize(products, 
              mic_colname=None, 
              noise_colname=None, 
              water_colname=None, 
              wireless_colname=None,
              type_colname=None):
    #IGNORE: products[products['connection'] == 'wireless'] = 1
    
    # Do products['colname'].unique() for columns to see which categories to create
    
    # microphone
    if (mic_colname):
        if (len(mic_colname)):
            products.loc[products[mic_colname] == 'mic',mic_colname] = 1
        else:
            for mic in mic_colname:
                products.loc[products[mic] == 'mic',mic] = 1

    # noise
    if (noise_colname):
        if (type(noise_colname) == list):
            for noise in noise_colname:
                noise_fact_helper(products, noise)
        else:
            noise_fact_helper(products, noise_colname)
    
    # water
    if (water_colname):
        if (type(water_colname) == list):
            for water in water_colname:
                water_fact_helper(products, noise)
        else:
            water_fact_helper(products, water_colname)
    
    # Wireless
    if (wireless_colname):
        if (type(water_colname) == list):
            for wireless in wireless_colname:
                is_wired = products[wireless].str.contains(r'wired', flags = re.I).replace(np.nan,True)
                products.loc[is_wired,wireless] = 'N'
                products.loc[-is_wired,wireless] = 'Y'
        else:
            is_wired = products[wireless_colname].str.contains(r'wired', flags = re.I).replace(np.nan,True)
            products.loc[is_wired,wireless_colname] = 'N'
            products.loc[-is_wired,wireless_colname] = 'Y'
        
    
    # This is for walmart
    #HeadphoneStyle: on ear will be overwritten if coexist with in/over ear
    #HeadphoneType
    #Type
    if (type_colname):
        if (type(type_colname) == list):
            for h_type in type_colname:
                type_fact_helper(products, h_type)
        else:
            type_fact_helper(products, type_colname)

