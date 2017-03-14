# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 18:56:06 2017


"""
import pandas as pd
import os.path 
from os import walk
def numeroActividad(actividad):
    numero = 0

    if(actividad=="ANDAR"):
        numero=1
    elif(actividad=="TROTAR"):
        numero=2
    elif(actividad=="BARRER"):
        numero=3
    return numero
                
    
    

def juntar():
     dfOutX = pd.DataFrame()
     dfOutY = pd.DataFrame()
    
    
     directorioActual=os.getcwd()
     
     for (path, ficheros, archivos) in walk("./DatosProcesados"):
        for i in  archivos:
           
            actividad=i.split('-')
            actividad=actividad[1]
            
            os.chdir(directorioActual+"/DatosProcesados")
            dfX=pd.DataFrame()
            dfX = pd.read_csv(i, sep=';', index_col=0, error_bad_lines=False)
           
            os.chdir(directorioActual)
            numero=numeroActividad(actividad)
           
            numeroFilas=len(dfX)
            
            dfY=pd.DataFrame()
            lista=list()
           
           
            d=0
            for d in range(numeroFilas):
                lista.append(numero)
            dfY=pd.DataFrame(lista)
          
            dfOutX = pd.concat([dfOutX, dfX])
            dfOutY = pd.concat([dfOutY, dfY])
     os.chdir(directorioActual)
     dfOutX.to_csv("X_train.csv",header=None, index=False)
     dfOutY.to_csv("y_train.csv",header=None, index=False)
            
if __name__ == "__main__":
    juntar()
            
        
    