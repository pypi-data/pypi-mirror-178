# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 13:58:12 2022

@author: NL5
"""
import json
from datetime import datetime

"fonction d ouverture du fichier JSON pour la sauvegarde des donnees"
def OUVRIR_json(fichier):
    with open(fichier) as f:
        return json.load(f)
"fonction d enregistrement des donnees dans le Fichier JSON"
def enregistrers(data):
    with open('soldeCaisseGenerale.json','w') as f:
        json.dump(data,f,indent=3)
"fonction de calcul de solde de la caisse qui recoit 3 parametres dont le solde initial du type decimal, la liste des encaissement du type liste et la liste des decaissement du type liste"   
def soldeCaisseGenerale(SoldeInitial,TableauEncaissement,TableauDecaissement):
   totalEncaissement=0;
   totalDecaissement=0;
   solde=SoldeInitial;
   
   for i in range(0,len(TableauEncaissement)):
       totalEncaissement+=TableauEncaissement[i]
       
   for ii in range(0,len(TableauDecaissement)):
       totalDecaissement+=TableauDecaissement[ii]
   solde=totalEncaissement-totalDecaissement
   "notre dictionaire qui reprend les donnees traitees"
   soldes={
                
        "totalEncaissement":totalEncaissement,
        "totalDecaissement":totalDecaissement,
        "solde":solde,
        "date":str(datetime.now()),
           
   }
   "ouverture du fichier de sauvegarde JSON pour la recuperation des anciennes informations"
   donnees=OUVRIR_json('soldeCaisseGenerale.json')
   "ajout du dictionaire a la liste"
   donnees.append(soldes)
   "enregistrement des modifications apporte au fichier JSON"
   enregistrers(donnees)
   
   "enfin on retourne le solde"
   return solde

" soldeCaisseGeneraleMonorange avec un parametre qui recoit la liste des Encaissements ou des decaissement et renvoi la sommation"
def soldeCaisseGeneraleMonorange(Tableau):
   totalEncaissement=0;   
   for i in range(0,len(Tableau)):
       totalEncaissement+=Tableau[i]
   
   
   return totalEncaissement



"fonction de solde cumulé de la caisse generale avec 3 parametres dont solde initial, liste des encaissment et la liste des decaissements"
def soldeCumilCaisseGenerale(SoldeInitial,TableauEncaissement,TableauDecaissement):
   totalEncaissement=0;
   totalDecaissement=0;
   solde=SoldeInitial;
   for i in range(0,len(TableauEncaissement)):
       totalEncaissement+=TableauEncaissement[i]
       solde=solde+totalEncaissement
       print(totalEncaissement)
  
   for ii in range(0,len(TableauDecaissement)):
       totalDecaissement+=TableauDecaissement[ii]
       solde=solde-totalEncaissement
       print(totalDecaissement)
   solde=0
   solde =totalEncaissement-totalDecaissement;
   return solde


"la fonction soldeCumilCaisseGenerale avec un parametre qui recoit la liste des Encaissements ou les decaissements et renvoi la somme cumulé avec les detaills"
def soldeCumilCaisseGeneraleMonoranger(Tableau):
   totalEncaissement=0;   
   for i in range(0,len(Tableau)):
       totalEncaissement+=Tableau[i]
       print(totalEncaissement)
   
   return totalEncaissement

"surcharge de la fonction soldeCumilCaisseGenerale avec un parametre qui recoit la liste des Decaissement et renvoi le total Decaissement"




"fonction de calcul de charge du personnel qui recoit le salaire de Base, liste des avantages et la liste des retenues"
def soldeComptePersonnel(salaireDeBase,ListeAvantage,ListeRetenue):
   totalAvantage=0;
   totalRetenu=0;
   solde=salaireDeBase;   
   for i in range(0,len(ListeAvantage)):
       totalAvantage+=ListeAvantage[i]
       print(totalAvantage)
   for ii in range(0,len(ListeRetenue)):
       totalRetenu+=ListeRetenue[ii]
       print(totalRetenu)
   solde=solde+totalAvantage-totalRetenu;
   return solde


"fonction de solde cumulé du tableau d exploitation avec 2 parametres dont liste des Produits et la liste des des charges"
def soldeCumulExploitation(TableauProduit,TableauCharge):
   totalProduit=0;
   totalCharge=0;
   solde=0;
   for i in range(0,len(TableauProduit)):
       totalProduit+=TableauProduit[i]
       solde=solde+totalProduit
       print(solde)
   for ii in range(0,len(TableauCharge)):
       totalCharge+=TableauCharge[ii]
       solde=solde-totalCharge
       print(solde)
   solde=0
   solde =totalProduit-totalCharge;
   return solde
"fonction de calcul de taux d amortissement qui recpoi en parametre 2 elements dont la vo=valeur d acquisition de l immobilisation et le n qui est la duree de vie de l immobilisqtion exprimnee en annee "
def annuite(vo,n):
    t=vo/n    
    return t

def durree(vo,annuite):
    durree=vo/annuite
    
    return durree
