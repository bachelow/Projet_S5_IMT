# Description:  
#    Trie les dossiers de manière à ce que ce soit beaucoup plus facile à les utiliser ensuite 

import pandas as pd
import numpy as np 
import os, shutil, csv


# Chemin où est stocké les données
root_dir = '../Data_participant_2019'
nom_finaux =  ['entrainement','facile','difficile','baseline']
nom_dossier = ['Cobaye','CSVFile']
fichier_csv = {'output_1':'HRV','output_2':'dp_d','output_3':'dp_g'}

# On calcule le nombre de sujet avec l'ensemble des dossiers présents 
nombre_dossier = len(os.listdir(root_dir))
compteur,compteur_baseline,numero_sujet = 0,0,0

liste_sujet = [1,2,3,4,5,6,7,8,9,10,11,12]
print(liste_sujet)
# On commence par créer des sous dossier Sujet_1, ..... Sujet_n s'ils n'existent pas
for sujet in liste_sujet:
	nouveau_dossier = 'Sujet_'+str(sujet)
	if not os.path.exists(os.path.join(root_dir,nouveau_dossier)):
		os.makedirs(os.path.join(root_dir,nouveau_dossier))
	else: 
		pass

for dossier_courant, dirs, files in os.walk(root_dir):

	if dossier_courant == root_dir:
			pass
	else: 
		# On regarde sur quel sujet on est: 
		if compteur == 6:
			compteur = 0
			numero_sujet+=1
		else:
			pass

		# On déplace tout les sous dossiers chez leurs sujets respectifs, on ne s'interesse pas au baseline pour le moment 
		for i,nom in enumerate(nom_dossier):
			if nom in dossier_courant and numero_sujet < 12:
				compteur+=1
				new_path = os.path.join(root_dir,'Sujet_'+str(liste_sujet[numero_sujet]))
				shutil.move(dossier_courant,new_path)
				print(dossier_courant, 'Sujet n° ',liste_sujet[numero_sujet])
				print('moved to ', new_path)

		# On déplace les baselines
		if 'Facelog' in dossier_courant and compteur_baseline < 12:
			new_path = os.path.join(root_dir,'Sujet_'+ str(liste_sujet[compteur_baseline]))
			compteur_baseline+=1
			shutil.move(dossier_courant,new_path)
			print('moved to ', new_path)

