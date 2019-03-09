# Ajoute une colonne de score ISA, une colonne délimitant deux états de fatigues et une avec 3 
# Au fichier csv présent dans les dossiers. 

############## Imports et variabes globales ##############

import pandas as pd
import numpy as np 
import os, shutil, csv


input_list = ['dp','HRV','ISA']
liste_sujet = [13,14] # A changer 
root_dir = '../Data_participant_2019'

############## Fonctions basiques ##############

def fill_tempo_list(csv_input,xlsx_dataframe,compteur_max):
	
	"""On associe à chaque valeure obtenue une valeure de score ISA et sa classe d'état de fatigue"""

	compteur = 1 
	list_tempo_isa,list_tempo_2_classes,list_tempo_3_classes = [],[],[]
	# On parcours les scores 
	for i in range(len(xlsx_dataframe[1])):

		isa = xlsx_dataframe[1][i]
		classe_2 = xlsx_dataframe[2][i]
		classe_3 = xlsx_dataframe[3][i]
		
		while compteur < compteur_max:
			list_tempo_isa.append(isa)
			list_tempo_2_classes.append(classe_2)
			list_tempo_3_classes.append(classe_3)
			compteur += 1
		
		compteur = 0

	# Comme les capteurs ont été allumés avant le début du scénario, on peut supposer que les valeurs au début 
	# Témoignent d'une situation nécessitant aucun effort mental (attente du participant). 
	# On traduit ça par des scores ISA de 1, et niveaau classification, à une appartenance au niveau 0 

	length_input, length_scores = len(csv_input), len(list_tempo_isa)
	diff = length_input - length_scores

	# Le but ici est de créer deux listes (diff_list_isa / diff_list_classes) telles que:
	# 		1. len(diff_list_isa) + len(list_tempo_isa) = length_input
	# 		2. les valeures du début de l'expérience soit associées aux scores ISA de la diff_list (cf plus haut pourquoi)
	# 		3. les scores suivant soient associés aux scores ISA du fichier excel 

	diff_list_isa = [1 for i in range(diff)]
	diff_list_classes = [0 for i in range(diff)]	

	liste_isa_finale = diff_list_isa + list_tempo_isa
	liste_2_classes_finale = diff_list_classes + list_tempo_2_classes
	liste_3_classes_finale = diff_list_classes + list_tempo_3_classes

	return liste_isa_finale,liste_2_classes_finale,liste_3_classes_finale

def adding_ISA_scores(csv_input,isa_input,directory=None):

	# On vérifie le nom de l'input (si c'est le diamètre pupillaire ou le HRV)
	input_name = os.path.splitext(csv_input)[0]
	
	# On transforme tou ça en dataframe 
	csv_input = pd.read_csv(csv_input,sep=';')
	xlsx_dataframe = pd.read_excel(isa_input,header=None)

	# Cas ou l'on traite les diamètres pupillaires
	if input_list[0] in input_name:

		# Les données du diamètre pupillaires sont récoltées toutes les 20 millisecondes
		# Celles des scores ISA toutes les 1 min 30. Il y a donc 4500 valeures qui ont le même score ISA
		liste_isa_finale, liste_2_classes_finale, liste_3_classes_finale = fill_tempo_list(csv_input,xlsx_dataframe,4500)

	# On traite le cas des HRV
	elif input_list[1] in input_name:

		# Les données du HRV sont récoltées à une fréquence un peu inférieure à 60 Hz (57,83)
		# Celles des scores ISA toutes les 1 min 30. Il y a donc environ 5000 valeures qui ont le même score ISA
		liste_isa_finale, liste_2_classes_finale, liste_3_classes_finale = fill_tempo_list(csv_input,xlsx_dataframe,4800)

	# Maintenant que les listes sont dans le bon sens on peut les ajouter au dataframe  
	csv_input[2] = liste_isa_finale
	csv_input[3] = liste_2_classes_finale
	csv_input[4] = liste_3_classes_finale

	# On sauvegarde 
	csv_input.to_csv(input_name + '_final.csv',header=None,index=False, sep=';')

############## Main ##############

if __name__ == '__main__':

	for sujet in liste_sujet:
		root_dir = os.path.join('../Data_participant_2019','Sujet_' + str(sujet))
		for dossier_courant, dirs, files in os.walk(root_dir):
			if dossier_courant == root_dir:
				pass
			else:
				# On ne s'interesse qu'au dossier CSVfile
				if 'CSVFile' in dossier_courant:
					print('Analyse du dossier ',dossier_courant)
				
					# On ne s'interesse qu'aux fichiers 
					for i,j,liste_fichier, in os.walk(dossier_courant): 
						for current_file_isa in liste_fichier:
							
							# Maintenant que l'on boucle sur les fichiers dans le bon dossier on peut commencer à modifier les csv
							nom_fichier_courant = os.path.splitext(current_file_isa)[0]

							# On stocke le chemin d'accès au fichier ISA 
							if input_list[2] in nom_fichier_courant:
								
								path_isa = os.path.join(dossier_courant,current_file_isa)
								print('ISA file found: ',path_isa) 
						
						print('Searching for HRV or pd input ...')
						for i in range(2):
							for current_file_input in liste_fichier:
								nom_fichier_courant = os.path.splitext(current_file_input)[0]
								# On vérifie si on est sur le bon fichier (dp_g / dp_d / HRV)
								if input_list[i] in nom_fichier_courant:
									
									path_input = os.path.join(dossier_courant,current_file_input)
									print('Adding ISA score to file ', path_input, ' ...')
									adding_ISA_scores(path_input,path_isa)
									
