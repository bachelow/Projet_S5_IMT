#functions to be used 

# required libraries
import numpy as np 
import os 
import pandas as pd


#counting number of files:

def number_of_files(path):
    n=0
    for file in os.listdir(path):
        if os.path.isfile(file):
            n+=1
    return(n)

def mask_hrv(file):
    mask = file['HRV'] == -1
    file = file[~mask]
    mask = file['HRV'] == 0
    file = file[~mask]   
    mask = file['HRV'] > 200
    file = file[~mask] 
    

def mask_eye(file,pos):
    #type = Left or Right
    mask = file['Diam Occ '+ pos] == 0
    file = file[~mask] 

 
def drop(file,n=3):
    file=file.drop(file.columns[:n],axis=1)
   
