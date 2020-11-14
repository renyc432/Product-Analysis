import json
import pandas as pd
import re


# helper: replace cells with 0 in these columns
def replace_blank(feat_ext_df, colnames):
    for feat in colnames:
        feat_ext_df[feat] = feat_ext_df[feat].replace(r'^\s*$', 0, regex=True)

feat_replace = ['connection','microphone','noise','water']


# warrenty: no warrent in about; prob in a different section of the website
#products[products['about_text_clean'].str.contains('warrent')].loc[:,'about_text_clean']

# driver type/unit size

# UPC

# MODEL NUMBER

# brand: search in Name; do not consider brand as a feature; this is more or less irrelevant to the analysis



def feature_extraction_helper (features_re, feat, product_desp):
    
    # battery: if battery_life < 4, then that is likely charging time
    if (feat == 'battery'):
        battery = re.findall(features_re['battery'],product_desp, re.I)    
        if (battery):
            #print(battery)
            battery_life = [i[0] for i in battery if float(i[0])>4]
            if (battery_life):           
                return max(battery_life)
            else:
                return ''
    
    if (feat == 'weight'):
        weight = re.search('(\d+(\.\d+)?)( )?(g|kg|oz|lb)', product_desp, re.I)
        if (weight):
            return weight.group()
        else:
            weight = re.search('(\w+)(weight)', product_desp, re.I)
            if (weight):
                return weight.group()
       
    if (feat == 'water'):
        water = re.search('water(\-| )?(proof|resist)', product_desp, re.I)
        if (water):
            return water.group()
        else:
            water = re.search('ipx[0-9]', product_desp, re.I)
            if (water):
                return water.group()
    
    text = re.search(features_re[feat], product_desp, re.I)
    if (text):
        return text.group()
    return ''


def feature_extraction(products, features_re):
    feat_ext_nested_list = []
    for product_description in products['about_text_clean']:
        feat_ext_row = [feature_extraction_helper(features_re, feat, product_description) for feat in features_re.keys()]
        feat_ext_nested_list.append(feat_ext_row)    
    feat_ext_df = pd.DataFrame(feat_ext_nested_list, columns = list(features_re.keys()))
    
    # replace empty cells
    replace_blank(feat_ext_df, feat_replace)
    
    feat_ext_df['connection'] = feat_ext_df['connection'].replace('bluetooth','wireless')
    return feat_ext_df






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
