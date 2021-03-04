import pandas as pd

# Returns a dataframe with flattened features and same number of rows as the original products
def list_flatten(products):
    
    # get all possible labels
    feat_labels = [label.split(',') for label in products['feat_labels_clean']]
    feat_labels_set = sum(feat_labels,[])
    feat_labels_set = set(feat_labels_set)
    feat_labels_set.remove('')
    
    flattened_feat = pd.DataFrame(columns=feat_labels_set)
    feat_values = [label.split(',') for label in products['feat_values_clean']]
    
    for i in range(len(feat_values)):
        flattened_feat = flattened_feat.append(dict(zip(feat_labels[i], feat_values[i])), ignore_index=True)
    
    flattened_feat = flattened_feat.drop('',axis=1)
    return flattened_feat