
#baseline mean and sd 


# required libraries
import numpy as np 
import math
import os 
import pandas as pd



#path containing data 
path='C:/Users/mbach/Desktop/TELECOM Bretagne/Projets/3A/S5/Code/Data_participant_2019'   # to change 

#list of subjects
n=len(os.listdir(path))
print("there is %d subjects" % n)

#list of dataframes
total= [None]*n     #will contain mean and sd 

for s in range(n):
    #looping through the number of subjects
    print("----------------------")
    new_path=path+'/Sujet_'+ str(s+1)
    facelog=[dir for dir in os.listdir(new_path) if dir[0]=='F']
    os.chdir(new_path+'/'+facelog[0])
    
    #creating the dataframe
    total[s]=pd.DataFrame()

    filename_HRV = 'Baseline_HRV_sujet_'+ str(s+1) +'.csv'
    filename_Eye = 'Baseline_Eye_sujet_'+ str(s+1) +'.csv'
    files = [filename_HRV, filename_Eye]


    for filename in files: 
        
        file = pd.read_csv(filename, sep = ',')
        

        file['Timestamp'] = file[file.columns[0]] 
        
        if filename == filename_HRV:

            mask = file['HR']==-1
            file = file[~mask]
            mask = file['HR']==0
            file = file[~mask]   
            mask = file['HR']>200
            file = file[~mask] 
            
            mean = file['HR'].mean()
            standard_dev = file['HR'].std()
            L = [mean, standard_dev]
            
    
        else : 
            mask = file['PUPIL_R_DIAM']==0
            file_diam_R = file[~mask]
                    
            mean = file_diam_R['PUPIL_R_DIAM'].mean()
            standard_dev = file_diam_R['PUPIL_R_DIAM'].std()
            M = [mean, standard_dev]
            
            mask = file['PUPIL_L_DIAM']==0
            file_diam_L = file[~mask]
                    
            mean = file_diam_L['PUPIL_R_DIAM'].mean()
            standard_dev = file_diam_L['PUPIL_R_DIAM'].std()
            N = [mean, standard_dev]
    print("----next subject----")        
            
    total[s] = pd.DataFrame([L, M, N],columns = ['Mean', 'Standard Deviation'] , index = ['HRV', 'Diam Right' ,'Diam Left'])
    os.chdir(new_path)
    total[s].to_csv('Baseline'+ str(s+1) +'.csv')
print("baseline csv for each subject is ready")
        