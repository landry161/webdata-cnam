import csv
import pandas as pd
import pdb
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use("webagg")
import webbrowser
import random
import numpy as np
import folium
from folium.plugins import MarkerCluster
import folium.plugins as plugins

def pieChartObjetsNonRestituesParAnnee():
	with open("objets_non_restitues_par_annee.csv") as output:
		result=csv.reader(output)
		labels=[]
		values=[]

		fig, ax = plt.subplots()
		for val in result:
			labels.append(str(val[0]))
			values.append(val[1])

		ax.pie(values, labels=labels, autopct='%1.1f%%')
		plt.title('Proportion des objets non restitués par an')
		plt.savefig("Resultats/objets_non_restitues_par_annee.png")

def pieChartObjetsRestituesParAnnee():
	with open("pie_chart_objets_restitues_par_annee.csv") as output:
		result=csv.reader(output)
		labels=[]
		values=[]

		fig, ax = plt.subplots()
		for val in result:
			labels.append(str(val[0]))
			values.append(val[1])

		ax.pie(values, labels=labels, autopct='%1.1f%%')
		plt.title('Proportion des objets restitués par an')
		plt.savefig("Resultats/objets_restitues_par_annee.png")

def mapOjetsRetrouvesParVilleParAn():
	with open("map_objets_retrouves_par_ville_par_an.csv") as output:
		result=csv.reader(output)
		boulder_coords = [46.7111,1.7191] #France
		my_map = folium.Map(location = boulder_coords,tiles='CartoDB dark_matter',zoom_start=6)
		marker_cluster = MarkerCluster().add_to(my_map)

		for val in result:
			ville=val[0]
			annee=val[1]
			latitude=val[2]
			longitude=val[3]
			total=val[4]

			if int(total)<100:
				myColor="green"
			else:
				myColor="white"

			tooltip=str(ville)+" année "+str(annee)
			folium.Marker([latitude,longitude],
				popup="<i>"+str(ville)+" avec "+str(total)+" objets retrouvé(e)s</i>",
				icon=plugins.BeautifyIcon(icon="arrow-down", icon_shape="marker",number=total,background_color=myColor),
				tooltip=tooltip).add_to(marker_cluster)
		my_map.save("Resultats/map_objets_retrouves_par_ville_par_an.html")
		webbrowser.open("Resultats/map_objets_retrouves_par_ville_par_an.html")

def mapNombreObjetsRetrouvesParDepartement():
	with open("map_nombre_objets_retrouves_par_departement.csv") as output:
		result=csv.reader(output)
		boulder_coords = [46.7111,1.7191] #France
		my_map = folium.Map(location = boulder_coords,tiles='Stamen Terrain',zoom_start=6)
		marker_cluster = MarkerCluster().add_to(my_map)
		for ele in result:
			departement=ele[0]
			lat=ele[1]
			lng=ele[2]
			nature_objets=ele[3]
			nombre_objets=ele[4]
			tooltip="Département "+str(departement)
			folium.Marker([lat,lng],
				popup="<i>"+str(nombre_objets)+" "+str(nature_objets)+" retrouvé(e)s</i>",
				tooltip=tooltip
				).add_to(marker_cluster)
		my_map.save("Resultats/map_nombre_objets_retrouves_par_departement.html")
		webbrowser.open("Resultats/map_nombre_objets_retrouves_par_departement.html")

def histogrammeGroupesObjetsRestituesNonRestituesParAn():
	anneeObjetsRestitues=[]
	valeurAnneeObjetsRestitues=[]

	anneeObjetsNonRestitues=[]
	valeurAnneeObjetsNonRestitues=[]

	with open("objets_non_restitues_par_annee.csv") as objNonRest:
		contentNonRestitues=csv.reader(objNonRest)

		for ele in contentNonRestitues:
			anneeObjetsNonRestitues.append(ele[0])
			valeurAnneeObjetsNonRestitues.append(int(ele[1]))

	with open("objets_restitues_par_annee.csv") as objRest:
		contentRestitues=csv.reader(objRest)

		for val in contentRestitues:
			anneeObjetsRestitues.append(str(val[0]))
			valeurAnneeObjetsRestitues.append(int(val[1]))

	x = np.arange(len(anneeObjetsRestitues))
	width = 0.35

	fig, ax = plt.subplots()
	rects1 = ax.bar(x - width/2, valeurAnneeObjetsRestitues, width, label='Restitués')
	rects2 = ax.bar(x + width/2, valeurAnneeObjetsNonRestitues, width, label='Non restitués')

	ax.set_ylabel("Nombres d''objets")
	ax.set_title('Histogramme groupé des objets restitués/non restitués par an')
	ax.set_xticks(x, anneeObjetsRestitues)
	ax.legend()

	ax.bar_label(rects1, padding=3)
	ax.bar_label(rects2, padding=3)

	fig.tight_layout()
	plt.savefig("Resultats/histogramme_groupes_des_objets_retrouves_et_non_restitutes.png")


def histogrammeObjetsRecuperesParRegion():
	df=pd.read_csv("histogramme_objets_recuperes_par_region.csv",sep=',',encoding_errors='ignore')
	labelsRegions=[]
	labelNombre=[]

	for d in df.index:
		labelsRegions.append(str(df.iloc[d][0]))
		labelNombre.append(df.iloc[d][1])
	
	plt.rcdefaults()
	fig, ax=plt.subplots()
	abscisse=np.arange(len(labelsRegions))
	error = np.random.rand(len(df))
	ax.barh(abscisse, labelNombre, xerr=error, align='center')

	for i,v in enumerate(labelNombre):
		ax.text(v+3, i+.25, str(v),color='blue', fontweight="bold")
	
	ax.set_yticks(abscisse, labels=labelsRegions)
	ax.invert_yaxis()
	ax.set_xlabel("Nombre d'objets")
	ax.set_title('Histogramme des objets récuperés par region?')
	
	plt.savefig("Resultats/histogramme_objets_recuperes_par_region.png")
	

def nuageDePointsObjetsDecouvertsParAn():
	compteurColor=0
	labelsYears=[]
	labelsObjects=[]
	labels_bar=[]
	bar_colors=[]

	with open("nuage_de_points_objets_decouverts_par_an.csv") as output:
		content=csv.reader(output)

		for j in content:
			labelsYears.append(j[0])
			labelsObjects.append(int(j[1]))
			compteurColor=compteurColor+1
			bar_colors.append(compteurColor)
	
		width = 0.5
		fig, ax = plt.subplots()
		
		scatter=plt.scatter(labelsYears,labelsObjects,s=200,c=bar_colors)
		plt.title("Nuage de Points du nombre d'objets découverts par année")
		plt.legend(handles=scatter.legend_elements()[0], labels=labelsObjects)
		plt.savefig("Resultats/nuages_de_points_objets_retrouves_par_annee.png")

#Appel de fonction
nuageDePointsObjetsDecouvertsParAn()
histogrammeGroupesObjetsRestituesNonRestituesParAn()
mapOjetsRetrouvesParVilleParAn()
pieChartObjetsRestituesParAnnee()
pieChartObjetsNonRestituesParAnnee()
histogrammeObjetsRecuperesParRegion()
mapNombreObjetsRetrouvesParDepartement()
print("Génération des resultats terminée")
print("Résultats disponibles dans le dossier Statitiques")