# Description:  
#    Trie les fichiers de manière à ce que ce soit beaucoup plus facile à les utiliser ensuite 

import pandas as pd
import numpy as np 
import os, shutil, csv
from txt_to_csv import txt_to_csv_fn

# Chemin où est stocké les données
root_dir = '../Data_participant_2019'
nom_finaux =  ['entrainement','facile','difficile']
nom_dossier = ['Cobaye','CSVFile','Facelog']
fichier_csv = {'output_1':'HRV','output_2':'dp_d','output_3':'dp_g'}

# On calcule le nombre de sujet avec l'ensemble des dossiers présents 
nombre_dossier = len(os.listdir(root_dir))
compteur = 0
liste_sujet = [1,2,3,4,5,6,7,8,9,10,11,12]

# Maintenant on parcours sujet par sujet et on change le nom des dossier et des fichiers 
# On initialise un compteur pour séparer les fichiers entraintement / facile et difficiles
compteur = 0
for sujet in liste_sujet:
	root_dir = os.path.join('../Data_participant_2019','Sujet_' + str(sujet))
	for dossier_courant, dirs, files in os.walk(root_dir):
		if dossier_courant == root_dir:
			pass
		else:
			print('Analyse du dossier ',dossier_courant)
			# On va dans le dossier contenant les csv
			if nom_dossier[1] in dossier_courant:
				# On ne s'interesse qu'aux fichiers, qui sont stockés dans la liste liste_fichier retourné par os.walk()
				for i,j,liste_fichier, in os.walk(dossier_courant):
					for name in fichier_csv:
						for current_file in liste_fichier:	

							# On stocke le nom du fichier 
							nom_fichier_courant = os.path.splitext(current_file)[0]
							if name in nom_fichier_courant and 'output_10' not in nom_fichier_courant and 'output_11' not in nom_fichier_courant and 'output_12' not in nom_fichier_courant:
								print(fichier_csv[name],' output found')
								path = os.path.join(dossier_courant,nom_fichier_courant+'.csv')

								# On renomme le fichier
								final_path = os.path.join(dossier_courant,fichier_csv[name]+'_'+nom_finaux[compteur]+'.csv')
								os.rename(path,final_path)
								print('Output renamed into', nom_finaux[compteur])
				compteur+=1

			# Maintenant on s'occupe de la baseline
			elif nom_dossier[2] in dossier_courant:
				for i,j,liste_fichier, in os.walk(dossier_courant):
					for current_file in liste_fichier:
						nom_fichier_courant = os.path.splitext(current_file)[0]
						extension = os.path.splitext(current_file)[1]

						# On regarde la baseline du HRV 
						if 'Summary' in nom_fichier_courant: 
							print('HRV Baseline found')
							path = os.path.join(dossier_courant,nom_fichier_courant+'.csv')
							
							# On renomme le fichier
							final_path = os.path.join(dossier_courant,'Baseline_HRV_sujet_'+ str(sujet) +'.csv')
							os.rename(path,final_path)
							print('Baseline renamed to: Baseline_HRV_sujet_'+ str(sujet))
						
						# On regarde pour les yeux: c'est le seul fichier texte présent dans le dossier
						elif extension == '.txt':
							print('Pupillary diameter Baseline found')
							path = os.path.join(dossier_courant,nom_fichier_courant+'.txt')
							final_path = os.path.join(dossier_courant,'Baseline_Eye_sujet_'+ str(sujet) +'.csv')
							
							txt_to_csv_fn(path,final_path)
							print('Baseline for subject ',sujet,' saved into csv')

	compteur = 0 
