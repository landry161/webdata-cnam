#fusion de deux fichiers .csv
import csv
import pdb
import pandas as pd
import numpy as np

objets=pd.DataFrame()
city=pd.DataFrame()

def formatDateValue(dateValue):
	if len(str(dateValue))<=3:
		return "1970"
	else:
		return dateValue.split("-")[0]

#Fonction de formatage des fichiers des objets retrouvés
def formatageFichierRetrouves():
	fileformate=open("objet-retrouves.csv","w")
	fileformate.write("code_uic;date;date_restitution;gare;nature_objets;type_objets;annee;annee_restitution"+"\n")

	fileNonDefini=open("donnees-manquantes-objets.csv","w")
	fileNonDefini.write("date;date_restitution;gare;nature_objets;type_objets"+"\n")

	with open("objets-trouves-restitution.csv","r",encoding="utf8") as output:
		csvValue=csv.reader(output,delimiter=";")
		header=next(csvValue)
		for value in csvValue:
			if len(value[3])==0 or len(value[2])==0:
				fileNonDefini.write(value[0]+";"+value[1]+";"+value[2]\
					+";"+value[3]+";"+value[4]+"\n")
			else:
				code_uic=int(value[3])
				annee_decouverte=formatDateValue(value[0])
				anne_restitution=formatDateValue(value[1])
				fileformate.write(str(code_uic)+";"+value[0]\
					+";"+value[1]+";"+value[2]+";"+value[4]+";"\
					+value[5]+";"+annee_decouverte\
					+";"+anne_restitution+"\n")

def genererFichierFinal():
	objets=pd.read_csv("objet-retrouves.csv",sep=";",encoding_errors='ignore')
	city=pd.read_csv("fichier-city-formate.csv",sep=";",encoding_errors='ignore')

	fichierFinal=open("Final.csv","w")
	fichierFinal.write("code_uic;date;date_restitution;gare;ville;villegare;region;departement;nature_objets;type_objets;annee_decouverte;annee_restitution;lat;lng"+"\n")
	for i in range(0,len(objets)):
		for j in range(0,len(city)):
			if objets._get_value(i,"code_uic")==city._get_value(j,"code_uic"):
				codeuic=objets._get_value(i,"code_uic")
				date=objets._get_value(i,"date")
			
				if len(str(objets._get_value(i,"date_restitution")))<=3:
					date_restitution=str("1970-01-01")
				else:
					date_restitution=str(objets._get_value(i,"date_restitution"))
			
				gare=objets._get_value(i,"gare")
				ville=city._get_value(j,"ville")
				villegare=city._get_value(j,"villegare")
				lat=str(city._get_value(j,"lat"))
				lng=str(city._get_value(j,"lng"))
				region=str(city._get_value(j,"region"))
				departement=str(city._get_value(j,"departement"))
				annee_decouverte=str(objets._get_value(i,"annee"))
				annee_restitution=str(objets._get_value(i,"annee_restitution"))
				nature_objets=objets._get_value(i,"nature_objets")
				type_objets=objets._get_value(i,"type_objets")

				print("Ligne "+str(i)+" écrite")
				fichierFinal.write(str(codeuic)+";"+date+";"+date_restitution+";"+gare+";"+ville+";"+villegare+";"+region+";"+departement+";"+nature_objets+";"+type_objets+";"+annee_decouverte+";"+annee_restitution+";"+lat+";"+lng+"\n")
'''
Fonction de génération du fichier de localisation des 
villes,region et de leur localisation
'''
def generateFichierCityLocationByCodeUI():
	with open("referentiel-gares-voyageurs.csv","r",encoding="utf8") \
	as resultCSV:
		value=csv.reader(resultCSV,delimiter=";")
		header=next(value)

		with open("fichier-city-formate.csv","w",newline='',\
			encoding="utf8") as fichier:
			writer = csv.DictWriter(fichier, delimiter=';',\
				fieldnames=["code_uic","ville","villegare","region",\
				"departement","lat","lng"])
			writer.writeheader()

			for ele in value:
				villegare=ele[25]
				lat=ele[11]
				lng=ele[10]
				region=ele[23]
				departement=ele[9]
				fichier.write(str(int(ele[2]))+";"+\
					ele[4]+";"+villegare+";"+region+\
					";"+departement+";"+str(lat)+";"+str(lng)+"\n")

#Appel de fonction
generateFichierCityLocationByCodeUI()
formatageFichierRetrouves()
genererFichierFinal()
pdb.set_trace()