
param_retailer = {}

walmart = {}
bestbuy = {}
param_retailer['walmart'] = walmart
param_retailer['bestbuy'] = bestbuy

################################### WALMART ####################################
walmart['colnames'] = {
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


walmart['features_re'] = {'brand':'(\w+)',
            # connection: if both wireless and wired (detachable cable), then it's considered wireless
            'connection':'bluetooth|wireless',
            'type': '(in|on|over)(-the)?(\-| )ear',
            'battery':'(\d+(\.\d+)?)+(\+)?( )?(hour|hours|hrs)',
            'microphone':'mic',
            'noise': '(noise|sound)(\-| )?(cancel|reduct|isolat)(\w+)',
            'water': 'water(\-| )?(proof|resist)',
#            'ipx':'ipx[0-9]',
#            'cord':'TODO: cord',
#            'warranty':'TODO: warranty',
            'weight':'(\d+(\.\d+)?)( )?(g|kg|oz|lb|lbs)',
#            'driver': 'TODO: driver',
            'impedance': '(\d)( )?(ohms)',
            'frequency response': '(\d+)( )?(hertz|hz|kilohertz|khz)',
            'sensitivity': '(\d+)( )?(decibels|decibel|db)( adjusted)?',
            'UPC': 'UPC(:)?(\s+)?(\d+)',
#            'model number': 'UPC(:)?(\s+)?(\d+)',
            'manufacturerID': '(manufacturer|mfr|model)(_|\s)?(number|#|ID|model)?( is)?(\s)?(:)?(\s+)?[\w\-/+]+'
    }




################################### bestbuy ####################################
bestbuy['colnames'] = {
    # colname: name of product
    'COLNAME_TITLE': 'name',
    # colname: retailer ID
    'COLNAME_RETAILER_ID': '',
    # colname: rating
    'COLNAME_RATING': 'rating',
    # colname: number of ratings
    'COLNAME_NUM_RATING': 'rating_amount',
    # colname: price
    'COLNAME_PRICE': 'price',
    # Colnames of about / description
    'COLNAME_ABOUT': ['general', 'key_specs','audio', 'connectivity', 'features','design','power','other'],
    # Colnames of features in ['wireless', 'type'] format
    'COLNAME_FEAT_LABELS': '',
    'COLNAME_FEAT_VALUES': ''
    }


bestbuy['features_re'] = {'brand':'(\w+)',
            'connection':'bluetooth|wireless',
            'type': '(in|on|over)(-the)?(\-| )ear',
            'battery':'(\d+(\.\d+)?)+(\+)?( )?(hour|hours|hrs)',
            'microphone':'mic',
            'noise': '(noise|sound)(\-| )?(cancel|reduct|isolat)(\w+)',        # This needs modification for bestbuy
            'water': 'water(\-| )?(proof|resist)',
#            'ipx':'ipx[0-9]',
#            'cord':'TODO: cord',
#            'warranty':'TODO: warranty',
            'weight':'(\d+(\.\d+)?)( )?(g|kg|oz|lb|lbs)',
#            'driver': 'TODO: driver',
            'impedance': '(\d)( )?(ohms)',
            'frequency response': '(\d+)( )?(hertz|hz|kilohertz|khz)',
            'sensitivity': '(\d+)( )?(decibels|decibel|db)( adjusted)?',
            'UPC': 'UPC(:)?(\s+)?(\d+)',
#            'model number': 'UPC(:)?(\s+)?(\d+)',
            'manufacturerID': '(manufacturer|mfr|model)(_|\s)?(number|#|ID|model)?( is)?(\s)?(:)?(\s+)?[\w\-/+]+'
    }

