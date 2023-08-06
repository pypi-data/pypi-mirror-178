# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 13:58:12 2022

@author: NL5
"""
"fonction de calcul duq solde de la caisse en prenant la liste des encaissement et la liste des decaissement en renvoi le solde final(liquidite disponible)"
def soldeCaisseGenerale(SoldeInitial,TableauEncaissement,TableauDecaissement):
   totalEncaissement=0;
   totalDecaissement=0;
   solde=SoldeInitial;
   for i in range(0,len(TableauEncaissement)):
       totalEncaissement+=TableauEncaissement[i]
   
   for ii in range(0,len(TableauDecaissement)):
       totalDecaissement+=TableauDecaissement[ii]
   solde=solde+totalEncaissement-totalDecaissement;
   return solde
"surcharge de la fonction soldeCaisseGeneral avec un parametre qui recoit la liste des Encaissements et renvoi le total encaissement"
def soldeCaisseGenerale(TableauEncaissement):
   totalEncaissement=0;   
   for i in range(0,len(TableauEncaissement)):
       totalEncaissement+=TableauEncaissement[i]
   
   
   return totalEncaissement

"surcharge de la fonction soldeCaisseGeneral avec un parametre qui recoit la liste des Decaissement et renvoi le total Decaissement"

def soldeCaisseGenerale(TableauDecaissement):
   totalDecaissement=0;   
   for i in range(0,len(TableauDecaissement)):
       totalDecaissement+=TableauDecaissement[i]
   
   
   return totalDecaissement

"fonction de solde cumulé de la caisse generale avec 3 parametres dont solde initial, liste des encaissment et la liste des decaissements"
def soldeCumilCaisseGenerale(SoldeInitial,TableauEncaissement,TableauDecaissement):
   totalEncaissement=0;
   totalDecaissement=0;
   solde=SoldeInitial;
   for i in range(0,len(TableauEncaissement)):
       totalEncaissement+=TableauEncaissement[i]
       solde=solde+totalEncaissement
       print(solde)
   for ii in range(0,len(TableauDecaissement)):
       totalDecaissement+=TableauDecaissement[ii]
       solde=solde-totalEncaissement
       print(solde)
   solde=0
   solde =totalEncaissement-totalDecaissement;
   return solde


"surcharge de la fonction soldeCumilCaisseGenerale avec un parametre qui recoit la liste des Encaissements et renvoi le total encaissement"
def soldeCumilCaisseGenerale(TableauEncaissement):
   totalEncaissement=0;   
   for i in range(0,len(TableauEncaissement)):
       totalEncaissement+=TableauEncaissement[i]
       print(totalEncaissement)
   
   return totalEncaissement

"surcharge de la fonction soldeCumilCaisseGenerale avec un parametre qui recoit la liste des Decaissement et renvoi le total Decaissement"

def soldeCumilCaisseGenerale(TableauDecaissement):
   totalDecaissement=0;   
   for i in range(0,len(TableauDecaissement)):
       totalDecaissement+=TableauDecaissement[i]
       print(totalDecaissement)
   
   return totalDecaissement


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
def TauxAmortissement(vo,n):
    t=vo/n
    
    return t
"fonctionde calcul de l annuite qui recoit le t=taux d amortissement et le vo=la valeur d acquisition "
def annuite(vo,t):
    annuite=vo*t
    return annuite

"surchare de la fonctionde calcul de l annuite qui recoit le t=taux d amortissement , le vo=la valeur d acquisition et le n pour l enregistrement des annuite dans json"
def annuite(vo,t,n):
    annuite=vo*t
    for i in range(0,n):        
        print(annuite)
    return annuite
    
    