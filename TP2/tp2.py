import sys
import numpy as np
from collections import Counter
import pandas as pd 
import math as ma

def main(): #!esto es temporal
    datos = [] 
    df = pd.DataFrame(columns=["palabras", "apariciones", "probabilidad"])
    datos = lecturaBin()
    diccionario = Counter(datos) 
    df = frameDeDatos(datos, df)
    alfabeto = creaAlfabeto(df)
    print(alfabeto)
    E = calcEntriopia(df,alfabeto)
    print(E)
    print(calcLong(df))
    
    
def lecturaBin(): 
    try:
        archivo = open("TP2/Samples/tp2_sample0.txt") #todo: agregar el sys.arg[2]
        datos = archivo.read()
        data = datos.split(" ")        
        archivo.close()
        return data
    except FileNotFoundError: 
        print("El archivo {filename} no existe") 
        return None


def frameDeDatos(datos, df): 
    diccionario = Counter(datos) 
    tot = diccionario.total()
    print(diccionario.keys)
    for key in diccionario: 
        nwRow = {"palabras": key, "apariciones": diccionario[key], "probabilidad": diccionario[key]/tot}
        df = df._append(nwRow, ignore_index = True)
    
    print(df)
    return df


def creaAlfabeto(df): 
    alfabeto = Counter()
    for word in df["palabras"]:  
        alfabeto += Counter(word)
    return alfabeto.keys()


#Prob * Log(en base a la cantidad de simbolos) (1 / prob)
def calcEntriopia(df, alfabeto): 
    base = len(alfabeto)
    E = 0
    for pro in df["probabilidad"]:
        E += (pro * ma.log(1/pro,base))
    return E

def calcLong(df): 
    sum = 0
    cant = 0
    for word in df["palabras"]:  
        sum += len(word)
        cant += 1
    return sum/cant



if __name__ == "__main__":
    main()