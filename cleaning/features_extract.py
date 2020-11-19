import numpy as np
import pandas as pd
import re


#test = 'manufacturerID: 3212-da_wd'
#re.search('(manufacturer|mfr|model)?(_|\s)?(number|#|ID|model)?( is)?(\s)?(:)?(\s+)?[\w\-+]+',test)

# helper: replace cells with 0 in these columns
def replace_blank(products, feat_colnames):
    for feat in feat_colnames:
        products[feat] = products[feat].replace(r'^\s*$', 0, regex=True)


# extracts numbers from columns;
# there must be only one number in the cell; 
# if more than one is present, the first number must be the target number
def numeric_extract(products, colnames_numeric):
    if (type(colnames_numeric) == list):
        for col in colnames_numeric:
            products[col] = [re.search('(\d+)', ID, re.I).group()
                             if type(ID) == str else np.nan for ID in products[col]]
    else:
        products[colnames_numeric] = [re.search('(\d+)', ID, re.I).group() 
                                      if type(ID) == str else np.nan for ID in products[colnames_numeric]]

# extracts the last element of the string
def mfrID_extract(products, colname_mfrID):
    products[colname_mfrID] = [ID.split()[-1] 
                               if type(ID) == str else np.nan for ID in products[colname_mfrID]]


def feat_ext_helper (features_re, feat, product_desp):
    
    # battery: if battery_life < 5, then that is likely charging time
    if (feat == 'battery'):
        battery = re.findall(features_re['battery'], product_desp, re.I)    
        if (battery):
            #print(battery)
            battery_life = [i[0] for i in battery if float(i[0])>5]
            if (battery_life):           
                return max(battery_life)
            else:
                return np.nan
    
    if (feat == 'weight'):
        #product_desp = 'awdad:11.22lb12312'
        weight = re.search(features_re['weight'], product_desp, re.I)
        if (weight):
            return weight.group()
        else:
            weight = re.search('(\w+)(weight)', product_desp, re.I)
            if (weight):
                return weight.group()
            else:
                return np.nan
       
    if (feat == 'water'):
        water = re.search(features_re['water'], product_desp, re.I)
        if (water):
            return water.group()
        else:
            water = re.search('ipx[0-9]', product_desp, re.I)
            if (water):
                water_text = water.group()
                if (int(water_text[3]) >= 5):
                    return 'water proof'
                else:
                    return 'water resist'
        return np.nan
    
    if (feat == 'connection'):
        connection = re.search(features_re['water'], product_desp, re.I)
        if (connection):
            return 1
        else:
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
    
    feat_ext_df['connection'] = feat_ext_df['connection'].replace('bluetooth','wireless')
    return feat_ext_df


#test = 'Bose headphone quiet noise cancelling'
#re.search('(\w+)',test)



    
    

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
    is_zero = pd.Series([bool(i+j+k) for i,j,k in zip(is_on,is_in,is_over)], index = products.index)
    
    products.loc[is_on,type_in] = 'on'
    products.loc[is_in,type_in] = 'in'
    products.loc[is_over,type_in] = 'over'
    products.loc[-is_zero,type_in] = np.nan

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


    
    
# =============================================================================
# 
# # join more than one datasets
# num_pages = 6
# products = []
# for i in range(1,num_pages+1):
#     file = 'laptop_page'+str(i)+'.json'
#     print(file)
#     with open(file,'rb') as fin:
#         content = json.load(fin)
#     print('page',i,'loaded successfully')
#     products = products + (content['products']) 
#     
# =============================================================================



# =============================================================================
# with open('laptop.json', 'w') as fout:
#     json.dump(products,fout,indent=1)
# =============================================================================
