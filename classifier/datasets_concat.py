import pandas as pd
import numpy as np
import time

 # higher price takes precendent bc the lower one may be sale price
    # wireless takes precedent bc a headphone can be both wireless and wired
    # higher battery takes precendent bc the lower one may be the charging time or the lower bound
def binary_merge(p1, p2):
    if (p1 is np.nan and p2 is np.nan):
        return np.nan
    if (p1 is np.nan):
        return p2
    if (p2 is np.nan):
        return p1
    if (p1 >= p2):
        return p1
    return p2


def noise_merge(n1,n2):
    if (n1 is np.nan and n2 is np.nan):
        return np.nan
    if (n1 is np.nan):
        return n2
    if (n2 is np.nan):
        return n1
    # isolate > cancel > reduct
    if (n1 == 'isolate' or n2 == 'isolate'):
        return 'isolate'
    if (n1 <= n2):
        return n1
    return n2

def type_merge(t1,t2):
    if (t1 is np.nan and t2 is np.nan):
        return np.nan
    if (t1 is np.nan):
        return t2
    if (t2 is np.nan):
        return t1
    # over > in > on
    if (t1 == 'over' or t2 == 'over'):
        return 'over'
    if (t1 >= t2):
        return t1
    return t2
    
def water_merge(w1, w2):
    if (w1 is np.nan and w2 is np.nan):
        return np.nan
    if (w1 is np.nan):
        return w2
    if (w2 is np.nan):
        return w1
    # proof > resist
    if (w1 <= w2):
        return w1
    return w2

def df_feat_merge(df):
    df['price'] = [binary_merge(p1,p2) for p1,p2 in zip(df['price_x'],df['price_y'])]
    df['num_rating'] = df['num_rating_x']+df['num_rating_y']
    df['rating'] = (df['rating_x']*df['num_rating_x'] + 
                    df['rating_y']*df['num_rating_y']) / df['num_rating']
    
    df['retailer'] = df['retailer_x']+','+df['retailer_y']
    df['_connection_'] = [binary_merge(c1,c2) for c1,c2 in zip(df['_connection__x'],df['_connection__y'])]
    df['_battery_'] = [binary_merge(b1,b2) for b1,b2 in zip(df['_battery__x'],df['_battery__y'])]
    df['_microphone_'] = [binary_merge(m1,m2) for m1,m2 in zip(df['_microphone__x'],df['_microphone__y'])]
    df['_noise_'] = [noise_merge(n1,n2) for n1,n2 in zip(df['_noise__x'],df['_noise__y'])]
    df['_type_'] = [type_merge(t1,t2) for t1,t2 in zip(df['_type__x'],df['_type__y'])]
    df['_water_'] = [water_merge(w1,w2) for w1,w2 in zip(df['_water__x'],df['_water__y'])]


def df_drop(df):
    df.drop(['price_x','rating_x','num_rating_x',
       '_connection__x', '_type__x', '_battery__x',
       '_microphone__x', '_noise__x', '_water__x', 'retailer_x',
       'name_y', 'price_y', 'rating_y', 'num_rating_y',
       '_connection__y', '_type__y', '_battery__y', '_microphone__y',
       '_noise__y', '_water__y', 'retailer_y'],axis=1,inplace=True)


def data_concat():
    path = 'C:\\Users\\roy79\\Desktop\\Research\\product-analysis'
    working_dir = path + '\\classifier'
    
    data_am = pd.read_csv(path+'\\clean_data\\amazon_hdphone_cleaned_col-combined.csv')
    data_bb = pd.read_csv(path+'\\clean_data\\bestbuy_hdphone_cleaned.csv')
    data_ne = pd.read_csv(path+'\\clean_data\\newegg_hdphone_cleaned_col-combined.csv')
    data_wm = pd.read_csv(path+'\\clean_data\\walmart_hdphone_cleaned.csv')
    
    data_am.rename({'rating_amount':'num_rating','ASIN':'retailer_ID'}, axis=1, inplace=True)
    
    data_bb.rename({'sku':'retailer_ID','rating_amount':'num_rating'}, axis=1, inplace=True)
    
    data_ne.rename({'Brand':'brand','model_ID':'model','Name':'name',
                    'num_of_rating':'num_rating','_price_':'price','_rating_':'rating'}, axis=1, inplace=True)
    
    data_wm.rename({'_model_':'model','walmart_id':'retailer_ID',
                    'rating_amount':'num_rating','_price_':'price'}, axis=1, inplace=True)
    
    data_ne['retailer_ID'] = np.nan
    
    data_am['retailer'] = 'amazon'
    data_bb['retailer'] = 'bestbuy'
    data_ne['retailer'] = 'newegg'
    data_wm['retailer'] = 'walmart'
    
    data_am = data_am[pd.notnull(data_am['name'])]
    data_bb = data_bb[pd.notnull(data_bb['name'])]
    data_ne = data_ne[pd.notnull(data_ne['name'])]
    data_wm = data_wm[pd.notnull(data_wm['name'])]
    
    data_list = [data_am, data_bb, data_ne, data_wm]
    
    # Match on UPC
    data_am_upc = data_am[pd.notnull(data_am._UPC_)]
    data_bb_upc = data_bb[pd.notnull(data_bb._UPC_)]
    data_ne_upc = data_ne[pd.notnull(data_ne._UPC_)]
    data_wm_upc = data_wm[pd.notnull(data_wm._UPC_)]
    
    data_upc = [data_am_upc,
                data_bb_upc,
                data_ne_upc,
                data_wm_upc]
    
    df_upc = []
    for i in range(0,len(data_upc)):
        for j in range(i+1,len(data_upc)):
            df_upc_temp = pd.merge(data_upc[i], 
                                   data_upc[j], 
                                   how = 'inner', on = '_UPC_')
            print(i,j,len(df_upc_temp))
            df_upc.append(df_upc_temp)
    
    df_upc = pd.concat(df_upc,axis=0)
    
    
    data_am.drop(['_UPC_','retailer_ID'],axis=1,inplace=True)
    data_bb.drop(['_UPC_','retailer_ID'],axis=1,inplace=True)
    data_ne.drop(['_UPC_','retailer_ID'],axis=1,inplace=True)
    data_wm.drop(['_UPC_','retailer_ID'],axis=1,inplace=True)
    
    
    
    data_am_model = data_am[pd.notnull(data_am.brand) & pd.notnull(data_am.model)]
    data_bb_model = data_bb[pd.notnull(data_bb.brand) & pd.notnull(data_bb.model)]
    data_ne_model = data_ne[pd.notnull(data_ne.brand) & pd.notnull(data_ne.model)]
    data_wm_model = data_wm[pd.notnull(data_wm.brand) & pd.notnull(data_wm.model)]
    
    data_model = [data_am_model,
                data_bb_model,
                data_ne_model,
                data_wm_model]
    
    
    df_model = []
    for i in range(0,len(data_model)):
        for j in range(i+1,len(data_model)):
            df_model_temp = pd.merge(data_model[i], 
                                   data_model[j], 
                                   how = 'inner', on = ['brand','model'])
            df_model.append(df_model_temp)
            print(i,j,len(df_model_temp))
         
            
         
   
    
    for df in df_model:
        df_feat_merge(df)
        df_drop(df)
        df.rename({'name_x':'name'}, axis=1, inplace=True)
    
    
    
    df_model_3 = []
    # am - bb - ne
    df_model_3.append(pd.merge(df_model[0], df_model[1], how = 'inner', on = ['brand','model']))
    # am - bb - wm
    df_model_3.append(pd.merge(df_model[0], df_model[2], how = 'inner', on = ['brand','model']))
    # am - ne - wm
    df_model_3.append(pd.merge(df_model[1], df_model[2], how = 'inner', on = ['brand','model']))
    # bb - ne - wm
    df_model_3.append(pd.merge(df_model[3], df_model[4], how = 'inner', on = ['brand','model']))
    
    
    for df in df_model_3:
        df_feat_merge(df)
        df_drop(df)
        df.rename({'name_x':'name'}, axis=1, inplace=True)
    
    
    df_model_4 = []
    df_model_4.append(pd.merge(df_model_3[0], df_model_3[1], how = 'inner', on = ['brand','model']))
    
    for df in df_model_4:
        df_feat_merge(df)
        df_drop(df)
        df.rename({'name_x':'name'}, axis=1, inplace=True)
    
    # products that have data from more than 2 retailers
    df_model_g2 = pd.concat(df_model_3+df_model_4,axis=0)
    
    df_model_2 = pd.concat(df_model,axis=0)
    is_in_g2 = (df_model_2['brand']+df_model_2['model']).isin(df_model_g2['brand']+df_model_g2['model'])
    
    # This is the final list of products that have same brand/model on multiple retailers
    df_model = pd.concat([df_model_2[-is_in_g2], df_model_g2], axis=0)
    
    # TODO: TRY MERGE ON NAME??
    
    
    is_brand_model_match_am = (data_am['brand']+data_am['model']).isin(df_model['brand']+df_model['model'])
    is_brand_model_match_bb = (data_bb['brand']+data_bb['model']).isin(df_model['brand']+df_model['model'])
    is_brand_model_match_ne = (data_ne['brand']+data_ne['model']).isin(df_model['brand']+df_model['model'])
    is_brand_model_match_wm = (data_wm['brand']+data_wm['model']).isin(df_model['brand']+df_model['model'])
    
    
    data_am_name = data_am[-is_brand_model_match_am]
    data_bb_name = data_bb[-is_brand_model_match_bb]
    data_ne_name = data_ne[-is_brand_model_match_ne]
    data_wm_name = data_wm[-is_brand_model_match_wm]
    
    
    # =============================================================================
    # 
    # data_am_name['name_split'] = [x.split() if type(x)==str else np.nan for x in data_am_name['name'] ]
    # data_bb_name['name_split'] = [x.split() if type(x)==str else np.nan for x in data_bb_name['name'] ]
    # data_ne_name['name_split'] = [x.split() if type(x)==str else np.nan for x in data_ne_name['name'] ]
    # data_wm_name['name_split'] = [x.split() if type(x)==str else np.nan for x in data_wm_name['name'] ]
    # 
    # data_am_name['name_split'] = data_am_name['name_split'].apply(lambda x: [w for w in x if w not in stopwords.words('english')])
    # data_bb_name['name_split'] = data_bb_name['name_split'].apply(lambda x: [w for w in x if w not in stopwords.words('english')])
    # data_ne_name['name_split'] = data_ne_name['name_split'].apply(lambda x: [w for w in x if w not in stopwords.words('english')])
    # data_wm_name['name_split'] = data_wm_name['name_split'].apply(lambda x: [w for w in x if w not in stopwords.words('english')])
    # 
    # freq_dist = [nltk.FreqDist(x) if type(x)==list else np.nan for x in data_am_name['name_split']]
    # =============================================================================
    
    
    # pd.concat all datasets
    
    data_all = pd.concat([data_am_name, data_bb_name, data_ne_name, data_wm_name,df_model])
    data_all['is_success'] = [r >= 4 if not pd.isnull(r) else np.nan for r in data_all['rating']]

    data_save_path = path + '\\clean_data\\'
    data_all.to_csv(data_save_path+'data_all'+time.strftime("%Y%m%d-%H%M%S")+'.csv', index=False)

data_concat()