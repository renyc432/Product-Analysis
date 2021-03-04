import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn import svm
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import statsmodels.api as sm

import matplotlib.pyplot as plt

path = 'C:\\Users\\roy79\\Desktop\\Research\\product-analysis'
working_dir = path + '\\cleaning'
data_path = path+'\\clean_data\\'+'data_all.csv'

data_all = pd.read_csv(data_path)

# clean['_microphone_'] = clean['_microphone_'].replace(np.nan, 0)

# drop columns not considered in classification
data_cl = data_all.drop(['name','num_rating','brand','model','retailer'],axis=1,inplace=False)

data_cl.drop('_battery_',axis=1,inplace=True)


# total dataset (w/ battery): 16062 -> 602
# total dataset (wo/ battery): 16062 -> 858
data_cl = data_cl.dropna(how='any')

data_cl = data_cl.astype({'price':'float64',
              '_noise_':'category',
              '_water_':'category'})

# create response variable
data_cl['is_success'] = data_cl['rating'] >= 4


# create dummy variables
_noise_dummy = pd.get_dummies(data_cl['_noise_'])
_water_dummy = pd.get_dummies(data_cl['_water_'])

data_cl = pd.concat([data_cl,_noise_dummy,_water_dummy],axis=1)

data_cl.drop(['rating','_type_','_noise_','_water_'],axis=1,inplace=True)

# Analysis Start

# y: rating
# classification: 
x_train, x_test, y_train, y_test = train_test_split(data_cl, 
                                                    data_cl['is_success'], 
                                                    test_size=0.3,random_state=321)
x_train.drop('is_success',axis=1,inplace=True)
x_test.drop('is_success',axis=1,inplace=True)


# XGBoost
cl_xgb = XGBClassifier(learning_rate=0.05,n_estimators=2000,max_depth=3)
cl_xgb.fit(x_train, y_train)
y_pred_xgb = cl_xgb.predict(x_test)
f1_xgb = f1_score(y_test, y_pred_xgb)
roc_auc_xgb = roc_auc_score(y_test, y_pred_xgb)
print('f1 socre - xgb: ', f1_xgb)
print('roc_auc socre - xgb: ', roc_auc_xgb)


def roc_auc_calc(alpha,n,depth, x_train, y_train, x_test, y_test):
    cl = XGBClassifier(learning_rate=alpha, n_estimators=n,max_depth=depth)
    cl.fit(x_train, y_train)
    y_pred = cl.predict(x_test)
    return roc_auc_score(y_test, y_pred)
    

# Fine tuning XGBoost
alphas = np.arange(0.04,0.1,0.01).tolist()
n_ests = np.arange(1000,2000,100).tolist()
depths = list(range(3,6))

scores_roc_auc_xgb = [(roc_auc_calc(a,n,d, x_train, y_train, x_test, y_test),a,n,d)
                      for a in alphas
                      for n in n_ests
                      for d in depths]
max(scores_roc_auc_xgb, key=lambda x:x[0])

# best: alpha = 0.06, n_estimators = 1200, max_depth = 4


###################### Other classification problems


# Logistic Regression
cl_log = LogisticRegression(max_iter=400)
cl_log.fit(x_train,y_train)
y_pred_log = cl_log.predict(x_test)
#mod_log.predict_proba(x_test_l)
f1_log = f1_score(y_test, y_pred_log)
roc_auc_log = roc_auc_score(y_test, y_pred_log)
print('f1 socre - log: ', f1_log)
print('roc_auc socre - log: ', roc_auc_log)


# Decision Tree
cl_tree = DecisionTreeClassifier(random_state = 321)
cl_tree.fit(x_train, y_train)
y_pred_tree = cl_tree.predict(x_test)
f1_tree = f1_score(y_test, y_pred_tree)
roc_auc_tree = roc_auc_score(y_test, y_pred_tree)
print('f1 socre - tree: ', f1_tree)
print('roc_auc socre - tree: ', roc_auc_tree)

# Random Forest
cl_forest = RandomForestClassifier(n_estimators= 1000)
cl_forest.fit(x_train,y_train)
y_pred_forest = cl_forest.predict(x_test)
f1_forest = f1_score(y_test, y_pred_forest)
roc_auc_forest = roc_auc_score(y_test, y_pred_forest)

# SVM
cl_svm = svm.SVC(kernel='rbf', probability=True)
cl_svm.fit(x_train, y_train)
y_pred_svm = cl_svm.predict(x_test)
f1_svm = f1_score(y_test, y_pred_svm)
roc_auc_svm = roc_auc_score(y_test, y_pred_svm) 
print('f1 socre - svm: ', f1_svm)
print('roc_auc socre - svm: ', roc_auc_svm)





###################### ROC

fpr, tpr, thresholds = roc_curve(y_test, cl_svm.predict_proba(x_test)[:,1])
plt.figure()
plt.plot(fpr,tpr, label = 'SVM (area= %0.2f)' % roc_auc_svm)
plt.plot([0,1],[0,1],'r--')
plt.title('ROC - SVM')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc="lower right")











