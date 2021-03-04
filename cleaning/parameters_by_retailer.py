
param_retailer = {}

walmart = {}
bestbuy = {}
newegg = {}
bhpv = {}
amazon = {}

param_retailer['walmart'] = walmart
param_retailer['bestbuy'] = bestbuy
param_retailer['newegg'] = newegg
param_retailer['bhpv'] = bhpv
param_retailer['amazon'] = amazon

################################### NEWEGG #####################################
newegg['factorize_conn_col'] = None
newegg['factorize_type_col'] = 'type'

newegg['colnames'] = {
    # colname: name of product
    'COLNAME_TITLE': 'Name',
    # colname: retailer ID
    'COLNAME_RETAILER_ID': '',
    # colname: model#
    'COLNAME_MODEL': '',
    # colname: rating
    'COLNAME_RATING': 'table_reviews_text',
    # colname: number of ratings
    'COLNAME_NUM_RATING': 'num_of_rating',
     # colname: current price
    'COLNAME_PRICE_CUR': 'price_current',
    # colname: original price
    'COLNAME_PRICE_ORIG': 'price_orig',
    # Colnames of about / description
    'COLNAME_ABOUT': ['overview',
                      'features',
                      'description',
                      'overview_table_text',
                      'specs_table_text'],
    # Colnames of features in ['wireless', 'type'] format
    'COLNAME_FEAT_LABELS': '',
    'COLNAME_FEAT_VALUES': ''
    }


newegg['features_re'] = {'_brand_':'(\w+)',
            # connection: if both wireless and wired (detachable cable), then it's considered wireless
            '_connection_':'bluetooth|wireless',
            '_type_': '(in|on|over)(-the)?(\-| )ear',
            '_battery_':'(\d+(\.\d+)?)+(\+)?( )?(hour|hours|hrs)',
            '_microphone_':'mic',
            '_noise_': '(noise|sound)(\-| )?(cancel|reduct|isolat)(\w+)',
            '_water_': 'water(\-| )?(proof|resist)',
#            '_ipx_':'ipx[0-9]',
#            '_cord_':'TODO: cord',
#            '_warranty_':'TODO: warranty',
            '_weight_':'(\d+(\.\d+)?)( )?(g|kg|oz|lb|lbs)',
#            '_driver_': 'TODO: driver',
            '_impedance_': '(\d)( )?(ohms)',
            '_frequency response_': '(\d+)( )?(hertz|hz|kilohertz|khz)',
            '_sensitivity_': '(\d+)( )?(decibels|decibel|db)( adjusted)?',
            '_UPC_': 'UPC(:)?(\s+)?(\d+)',
#            '_model number_': 'UPC(:)?(\s+)?(\d+)',
            '_manufacturerID_': '(manufacturer|mfr|model)(_|\s)?(number|#|ID|model)?( is)?(\s)?(:)?(\s+)?[\w\-/+]+'
    }

################################### WALMART ####################################
walmart['factorize_conn_col'] = None
walmart['factorize_type_col'] = '_type_'


walmart['colnames'] = {
    # colname: name of product
    'COLNAME_TITLE': 'name',
    # colname: retailer ID
    'COLNAME_RETAILER_ID': 'walmart_id',
    # colname: model#
    'COLNAME_MODEL': 'model',
    # colname: rating
    'COLNAME_RATING': 'rating',
    # colname: number of ratings
    'COLNAME_NUM_RATING': 'rating_amount',
    # colname: current price
    'COLNAME_PRICE_CUR': 'price_current',
    # colname: original price
    'COLNAME_PRICE_ORIG': 'price_original',
    # Colnames of about / description
    'COLNAME_ABOUT': ['about','specification'],
    # Colnames of features in ['wireless', 'type'] format
    'COLNAME_FEAT_LABELS': '',
    'COLNAME_FEAT_VALUES': ''
    }


walmart['features_re'] = {'_brand_':'(\w+)',
            # connection: if both wireless and wired (detachable cable), then it's considered wireless
            '_connection_':'bluetooth|wireless',
            '_type_': '(in|on|over)(-the)?(\-| )ear',
            '_battery_':'(\d+(\.\d+)?)+(\+)?( )?(hour|hours|hrs)',
            '_microphone_':'mic',
            '_noise_': '(noise|sound)(\-| )?(cancel|reduct|isolat)(\w+)',
            '_water_': 'water(\-| )?(proof|resist)',
#            '_ipx_':'ipx[0-9]',
#            '_cord_':'TODO: cord',
#            '_warranty_':'TODO: warranty',
            '_weight_':'(\d+(\.\d+)?)( )?(g|kg|oz|lb|lbs)',
#            '_driver_': 'TODO: driver',
            '_impedance_': '(\d)( )?(ohms)',
            '_frequency response_': '(\d+)( )?(hertz|hz|kilohertz|khz)',
            '_sensitivity_': '(\d+)( )?(decibels|decibel|db)( adjusted)?',
            '_UPC_': 'UPC(:)?(\s+)?(\d+)',
#            '_model number_': 'UPC(:)?(\s+)?(\d+)',
            '_manufacturerID_': '(manufacturer|mfr|model)(_|\s)?(number|#|ID|model)?( is)?(\s)?(:)?(\s+)?[\w\-/+]+'
    }




################################### AMAZON #####################################

### The parameters below can be determined by looking at the columns and variable types in the dataset
### However, some may not be obvious at first; and can be determined after we step through remove_used()
# used in features_extract.factorize()
amazon['factorize_conn_col'] = None
amazon['factorize_type_col'] = '_type_'

amazon['colnames'] = {
    # colname: name of product
    'COLNAME_TITLE': 'name',
    # colname: retailer ID
    'COLNAME_RETAILER_ID': 'ASIN',
    # colname: model#
    'COLNAME_MODEL': '',
    # colname: rating
    'COLNAME_RATING': 'rating',
    # colname: number of ratings
    'COLNAME_NUM_RATING': 'rating_amount',
    # colname: current price
    'COLNAME_PRICE_CUR': 'price',
    # colname: original price
    'COLNAME_PRICE_ORIG': '',
    # Colnames of about / description
    'COLNAME_ABOUT': ['about','product_description'],
    # Colnames of features in ['wireless', 'type'] format
    'COLNAME_FEAT_LABELS': '',
    'COLNAME_FEAT_VALUES': ''
    }


amazon['features_re'] = {'_brand_':'(\w+)',
            # connection: if both wireless and wired (detachable cable), then it's considered wireless
            '_connection_':'bluetooth|wireless',
            '_type_': '(in|on|over)(-the)?(\-| )ear',
            '_battery_':'(\d+(\.\d+)?)+(\+)?( )?(hour|hours|hrs)',
            '_microphone_':'mic',
            '_noise_': '(noise|sound)(\-| )?(cancel|reduct|isolat)(\w+)',
            '_water_': 'water(\-| )?(proof|resist)',
#            '_ipx_':'ipx[0-9]',
#            '_cord_':'TODO: cord',
#            '_warranty_':'TODO: warranty',
            '_weight_':'(\d+(\.\d+)?)( )?(g|kg|oz|lb|lbs)',
#            '_driver_': 'TODO: driver',
            '_impedance_': '(\d)( )?(ohms)',
            '_frequency response_': '(\d+)( )?(hertz|hz|kilohertz|khz)',
            '_sensitivity_': '(\d+)( )?(decibels|decibel|db)( adjusted)?',
            '_UPC_': 'UPC(:)?(\s+)?(\d+)',
#            '_model number_': 'UPC(:)?(\s+)?(\d+)',
            '_manufacturerID_': '(manufacturer|mfr|model)(_|\s)?(number|#|ID|model)?( is)?(\s)?(:)?(\s+)?[\w\-/+]+'
    }



##################################### BHPV #####################################

bhpv['factorize_conn_col'] = None
bhpv['factorize_type_col'] = None

bhpv['colnames'] = {
    # colname: name of product
    'COLNAME_TITLE': 'name',
    # colname: retailer ID
    'COLNAME_RETAILER_ID': 'bhpv_ID',
    # colname: model#
    'COLNAME_MODEL': '',
    # colname: rating
    'COLNAME_RATING': 'rating',
    # colname: number of ratings
    'COLNAME_NUM_RATING': 'num_of_rating',
    # colname: current price
    'COLNAME_PRICE_CUR': 'price',
    # colname: original price
    'COLNAME_PRICE_ORIG': '',
    # Colnames of about / description
    'COLNAME_ABOUT': '',
    # Colnames of features in ['wireless', 'type'] format
    'COLNAME_FEAT_LABELS': 'feat_labels',
    'COLNAME_FEAT_VALUES': 'feat_values'
    }


bhpv['features_re'] = {'_brand_':'(\w+)',
            # connection: if both wireless and wired (detachable cable), then it's considered wireless
            '_connection_':'bluetooth|wireless',
            '_type_': '(in|on|over)(-the)?(\-| )ear',
            '_battery_':'(\d+(\.\d+)?)+(\+)?( )?(hour|hours|hrs)',
            '_microphone_':'mic',
            '_noise_': '(noise|sound)(\-| )?(cancel|reduct|isolat)(\w+)',
            '_water_': 'water(\-| )?(proof|resist)',
#            '_ipx_':'ipx[0-9]',
#            '_cord_':'TODO: cord',
#            '_warranty_':'TODO: warranty',
            '_weight_':'(\d+(\.\d+)?)( )?(g|kg|oz|lb|lbs)',
#            '_driver_': 'TODO: driver',
            '_impedance_': '(\d)( )?(ohms)',
            '_frequency response_': '(\d+)( )?(hertz|hz|kilohertz|khz)',
            '_sensitivity_': '(\d+)( )?(decibels|decibel|db)( adjusted)?',
            '_UPC_': 'UPC(:)?(\s+)?(\d+)',
#            '_model number_': 'UPC(:)?(\s+)?(\d+)',
            '_manufacturerID_': '(manufacturer|mfr|model)(_|\s)?(number|#|ID|model)?( is)?(\s)?(:)?(\s+)?[\w\-/+]+'
    }


################################### bestbuy ####################################
bestbuy['factorize_conn_col'] = None
bestbuy['factorize_type_col'] = '_type_'

bestbuy['colnames'] = {
    # colname: name of product
    'COLNAME_TITLE': 'name',
    # colname: retailer ID
    'COLNAME_RETAILER_ID': '',
    # colname: model#
    'COLNAME_MODEL': '',
    # colname: rating
    'COLNAME_RATING': 'rating',
    # colname: number of ratings
    'COLNAME_NUM_RATING': 'rating_amount',
    # colname: current price
    'COLNAME_PRICE_CUR': 'price',
    # colname: original price
    'COLNAME_PRICE_ORIG': '',
    # Colnames of about / description
    'COLNAME_ABOUT': ['general', 'key_specs','audio', 'connectivity', 'features','design','power','other'],
    # Colnames of features in ['wireless', 'type'] format
    'COLNAME_FEAT_LABELS': '',
    'COLNAME_FEAT_VALUES': ''
    }



bestbuy['features_re'] = {'_brand_':'(\w+)',
            # connection: if both wireless and wired (detachable cable), then it's considered wireless
            '_connection_':'bluetooth|wireless',
            '_type_': '(in|on|over)(-the)?(\-| )ear',
            '_battery_':'(\d+(\.\d+)?)+(\+)?( )?(hour|hours|hrs)',
            '_microphone_':'mic',
            '_noise_': '(noise|sound)(\-| )?(cancel|reduct|isolat)(\w+)',
            '_water_': 'water(\-| )?(proof|resist)',
#            '_ipx_':'ipx[0-9]',
#            '_cord_':'TODO: cord',
#            '_warranty_':'TODO: warranty',
            '_weight_':'(\d+(\.\d+)?)( )?(g|kg|oz|lb|lbs)',
#            '_driver_': 'TODO: driver',
            '_impedance_': '(\d)( )?(ohms)',
            '_frequency response_': '(\d+)( )?(hertz|hz|kilohertz|khz)',
            '_sensitivity_': '(\d+)( )?(decibels|decibel|db)( adjusted)?',
            '_UPC_': 'UPC(:)?(\s+)?(\d+)',
#            '_model number_': 'UPC(:)?(\s+)?(\d+)',
            '_manufacturerID_': '(manufacturer|mfr|model)(_|\s)?(number|#|ID|model)?( is)?(\s)?(:)?(\s+)?[\w\-/+]+'
    }
