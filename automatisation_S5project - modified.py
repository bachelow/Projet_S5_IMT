#automatisation code 

# required libraries
import numpy as np 
import os 
import pandas as pd
import time
from module import *

print(os.getcwd(), '\n')


#path containing data 
path='C:/Users/mbach/Desktop/TELECOM Bretagne/Projets/3A/S5/Code/Data_participant_2019'   # to change 

#list of subjects
n=len(os.listdir(path))
print("there are %d subjects" % n)


start = time. time()

for s in range (12,14):
    
    new_path = path + '/Sujet_'+ str(s+1)

    #list of directories which contains the csv files
    all_dir=[dir for dir in os.listdir(new_path) if dir[-7:]=='CSVFile']

    number_of_dir= len(all_dir)
    print('number of directories',number_of_dir,'\n ',all_dir ,' ... etc ')

    #list of dataframes
    HRV_clean = [None]*number_of_dir
    HRV = [None]*number_of_dir
    Diam_Right_clean = [None]*number_of_dir
    Diam_Left_clean = [None]*number_of_dir
    
    os.chdir(new_path)
    total = pd.read_csv('Baseline'+ str(s+1) +'.csv')


    c=0    #counter (will be the index of the list in the next for-loop)

    
    for dir in all_dir:
        print("-------------")
        c+=1
        os.chdir(new_path+'/' + dir)

        print('--> ', os.getcwd())

        HRV_clean[c-1] = pd.DataFrame()
        HRV[c-1] = pd.DataFrame()
        Diam_Right_clean[c-1] = pd.DataFrame()
        Diam_Left_clean[c-1] = pd.DataFrame()

        scenarios = ['entrainement' ,'facile', 'difficile']
        filename_HRV = 'HRV_'+ scenarios[c-1] +'_final.csv'
        filename_pupleft = 'dp_g_'+ scenarios[c-1] +'_final.csv'
        filename_pupright = 'dp_d_'+ scenarios[c-1] +'_final.csv'

        files = [filename_HRV, filename_pupleft, filename_pupright]

        for filename in files: 
            file = pd.read_csv(filename, sep = ';')
            
            file['Timestamp'] = file[file.columns[0]] 
                    
            if filename == filename_HRV: 
                V = []
                file['HRV'] = file[file.columns[1]] 
                file = file.drop(file.columns[1],1)
                file.index = np.arange(1,len(file)+1)
                HRV[c-1] = pd.concat([HRV[c-1], file])

                for i in range(1,len(file), 50): 
                    V.append(i)
                for i in file.index: 
                    if i not in V : 
                        file = file.drop(i,0)

                mask = file['HRV'] == -1
                file = file[~mask]
                mask = file['HRV'] == 0
                file = file[~mask]   
                mask = file['HRV'] > 200
                file = file[~mask]            
                
                HRV_clean[c-1] = pd.concat([HRV_clean[c-1], file])



            elif filename == filename_pupleft : 
                file['Diam Occ Left'] = file[file.columns[1]] 
                file = file.drop(file.columns[1],1)
                mask = file['Diam Occ Left']==0
                file = file[~mask]
                
                Diam_Left_clean[c-1] = pd.concat([Diam_Left_clean[c-1], file])


            else : 
                file['Diam Occ Right'] = file[file.columns[1]] 
                file = file.drop(file.columns[1],1)
                mask = file['Diam Occ Right']==0
                file = file[~mask]
                
                Diam_Right_clean[c-1] = pd.concat([Diam_Right_clean[c-1], file])

        HRV_clean[c-1]['HRV centre'] = (HRV_clean[c-1]['HRV'] - total['Mean'][0]) / total['Standard Deviation'][0]
        Diam_Right_clean[c-1]['Diam Occ Right centre'] = (Diam_Right_clean[c-1]['Diam Occ Right'] - total['Mean'][1]) / total['Standard Deviation'][1]
        Diam_Left_clean[c-1]['Diam Occ Left centre'] = (Diam_Left_clean[c-1]['Diam Occ Left'] - total['Mean'][2]) / total['Standard Deviation'][2]


        print("next directory \n start process")

    print("--------------------")
    #list of dataframes are full 
    end = time. time()
    print('execution time for one subject  ===== ',end - start)


    #adding a column of the difficulty level for each dataframe in the list 

    for i in range(number_of_dir):
        HRV_clean[i].insert(0,'difficulty level',i+1 )
        Diam_Right_clean[i].insert(0,'difficulty level',i+1 )
        Diam_Left_clean[i].insert(0,'difficulty level',i+1 )
        
    # concatenation of the frames of each category to one dataframe per category 
    #  --> 3 csv files containing all data

    #path_for_csv=input('type the path where you want to save the files ^^ \n')

    HRV_final=pd.concat([frames for frames in HRV_clean],ignore_index=True)
    Diam_Left_final=pd.concat([frames for frames in Diam_Left_clean],ignore_index=True)
    Diam_Right_final=pd.concat([frames for frames in Diam_Right_clean],ignore_index=True)

    csv_files=[HRV_final,Diam_Left_final,Diam_Right_final]
    csv_names = ['HRV_final','Diam_Left_final','Diam_Right_final']

    for i,f in enumerate(csv_files):
        # f=f.drop(file.columns[:4],axis=1)
        f.to_csv(new_path+'/'+csv_names[i]+'.csv',sep=';')

    print("csv files ready for subject number  ", s+1)

print("-------------------------------------")
end2=time.time()
print("full execution time =======", end2-start)

    



        





