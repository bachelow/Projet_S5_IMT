# Script qui lance la classification pour adaboost et svm (La partie commentée)

############## Imports et variabes globales ##############

import numpy as np 
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svn import SVC 
from sklearn.model_selection import cross_val_score

df_pd_r = pd.read_csv('Pupillary_diam_right_concatenate.csv',sep=';')
df_pd_l = pd.read_csv('Pupillary_diam_left_concatenate.csv',sep=';')
df_hrv = pd.read_csv('HRV_concatenate.csv',sep=';')
liste_df = [df_pd_r,df_pd_l,df_hrv]
result_dict = {'2 Classes':[],'3 Classes':[]}
liste_metrique = ['Diam Occ Right centre','Diam Occ Left centre','HRV centre']

############## Script ##############

for i in range(2):
    
    print('Tests for a ' + str(i+2) + ' class classification')
    
    for j in range(3):
    
        print('classification for ',liste_df[j].head())
        data = liste_df[j]
        X = np.array(data[liste_metrique[j]])
        X = np.reshape(X,(-1,1))
        
        if i == 0:
            y = np.array(data['0'])
        else:
            y = np.array(data['0.1'])
        
        # On commence la classification 
        clf = AdaBoostClassifier(n_estimators=500,verbose=1)
        # clf = SVC(gamma='auto',kernel='rbf',decision_function_shape='ovo',verbose=3)
        print(clf)
        scores = cross_val_score(clf,X,y,cv=5)
        scores = scores.mean()
        print('scores obtenus: ',scores)
        
        if i == 0:
            result_dict['2 Classes'].append(scores)
        else:
            result_dict['3 Classes'].append(scores)
        
        print('-----------------------------------------')

path = 'données_adaboost'
np.savez_compressed(path,a=result_dict)
print('données sauvegardées')
        
        
