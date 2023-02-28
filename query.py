import csv
import pandas as pd
import pdb
from fugue_sql import fsql
import geopandas as gpd

df=pd.read_csv("Final.csv",sep=';',encoding_errors='ignore')

def pieChartObjetsRestituesParAnnee():
	query="""
	SELECT annee_restitution,count(nature_objets) AS TOTAL FROM df
	WHERE annee_restitution>1970
	GROUP BY annee_restitution
	SAVE OVERWRITE "H:/BOGBE JOSE LANDRY/Projet CNAM/Statistiques/pie_chart_objets_restitues_par_annee.csv"
	"""
	execute_query=fsql(query).run()

def mapOjetsRetrouvesParVilleParAn():
	query="""
	SELECT ville,annee_decouverte,lat,lng,count(annee_decouverte) AS TOTAL FROM df
	GROUP BY ville,annee_decouverte
	SAVE OVERWRITE "H:/BOGBE JOSE LANDRY/Projet CNAM/Statistiques/map_objets_retrouves_par_ville_par_an.csv"
	"""
	execute_query=fsql(query).run()

def objetNonRestitutesParAnnee():
	query="""
	SELECT annee_decouverte,count(*) AS TOTAL FROM df
	WHERE annee_restitution==1970
	GROUP BY annee_decouverte
	SAVE OVERWRITE "H:/BOGBE JOSE LANDRY/Projet CNAM/Statistiques/objets_non_restitues_par_annee.csv"
	"""
	execute_query=fsql(query).run()

def objetsRestituesParAnnee():
	query="""
	SELECT annee_decouverte, count(*) AS TOTAL FROM df
	WHERE annee_restitution!=1970
	GROUP BY annee_decouverte
	SAVE OVERWRITE "H:/BOGBE JOSE LANDRY/Projet CNAM/Statistiques/objets_restitues_par_annee.csv"
	"""
	execute_query=fsql(query).run()

def nuageDePointsObjetsDecouvertsParAn():
	query="""
	SELECT annee_decouverte, count(nature_objets) AS TOTAL FROM df
	WHERE annee_decouverte
	GROUP BY annee_decouverte
	SAVE OVERWRITE "H:/BOGBE JOSE LANDRY/Projet CNAM/Statistiques/nuage_de_points_objets_decouverts_par_an.csv"
	"""
	execute_query=fsql(query).run()

def histogrammeObjetsRecuperesParRegion():
	query="""
	SELECT region,count(*) AS TOTAL FROM df
	GROUP BY region
	SAVE OVERWRITE "H:/BOGBE JOSE LANDRY/Projet CNAM/Statistiques/histogramme_objets_recuperes_par_region.csv"
	"""
	execute_query=fsql(query).run()

def mapNombreObjetsRetrouvesParDepartement():
	query="""
	SELECT departement,lat,lng,nature_objets,count(nature_objets) AS total FROM df
	GROUP BY departement,nature_objets
	SAVE OVERWRITE "H:/BOGBE JOSE LANDRY/Projet CNAM/Statistiques/map_nombre_objets_retrouves_par_departement.csv"
	"""
	execute_query=fsql(query).run()

#Final
mapOjetsRetrouvesParVilleParAn()
nuageDePointsObjetsDecouvertsParAn()
histogrammeObjetsRecuperesParRegion()
objetNonRestitutesParAnnee()
objetsRestituesParAnnee()
pieChartObjetsRestituesParAnnee()
mapNombreObjetsRetrouvesParDepartement()
print("Génération des requêtes terminée.")