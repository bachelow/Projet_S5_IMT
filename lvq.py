# Script qui lance la classification pour LVQ
# La cross validation s'est faite à la "main" parce que cet LVQ de cet algo n'est pas compatible avec Sklearn 

############## Imports et variabes globales ##############

import numpy as np 
import pandas as pd
from neupy import algorithms
from sklearn.model_selection import cross_val_score,KFold
from sklearn import metrics

df_pd_r = pd.read_csv('Pupillary_diam_right_concatenate.csv',sep=';')
df_pd_l = pd.read_csv('Pupillary_diam_left_concatenate.csv',sep=';')
df_hrv = pd.read_csv('HRV_concatenate.csv',sep=';')
liste_df = [df_pd_r,df_pd_l,df_hrv]
result_dict = {'2 Classes':[],'3 Classes':[]}
liste_metrique = ['Diam Occ Right centre','Diam Occ Left centre','HRV centre']

############## Script ##############

for i in range(2):
        print('Tests for a ' + str(i+1) + ' classification')
        
        for j in range(3):
        
                data = liste_df[j]
                X = np.array(data[liste_metrique[j]])
                X = np.reshape(X,(-1,1))
                kfold = KFold(n_splits=5,shuffle=True)
                scores = []
                for train, test in kfold.split(X):
                        x_train, x_test = X[train], X[test]
                        
                        if i == 0:
                                y = np.array(data['0'])
                                y_train, y_test = y[train], y[test]
                                lvq = algorithms.LVQ3(n_inputs=1, n_classes=2)
                        else:
                                y = np.array(data['0.1'])
                                y_train, y_test = y[train], y[test]
                                lvq = algorithms.LVQ3(n_inputs=1, n_classes=3)
                  
                        lvq.train(x_train, y_train, epochs=50)
                        y_predicted = lvq.predict(x_test)
                        score = metrics.mean_absolute_error(y_test, y_predicted)
                        scores.append(score)
                scores = np.mean(scores)
                print('######################### scores obtenus: ',scores)
                if i == 0:
                        result_dict['2 Classes'].append(scores)
                else:
                        result_dict['3 Classes'].append(scores)
                print('-----------------------------------------')
        
path = 'donnees_lvq'
np.savez_compressed(path,a=result_dict)
print('donnees sauvegardees')
