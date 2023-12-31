import sys
import numpy as np
from collections import Counter
import pandas as pd 
import math as ma

def main(): 
    if len(sys.argv) < 2: 
        print("cabecera de archivo invalida") 
    else: 
        filename = sys.argv[1] 
        ejecuta(filename)


def ejecuta(filename): 
    datos = [] 
    df = pd.DataFrame(columns=["palabras", "apariciones", "probabilidad"])
    datos = lecturaBin(filename)
    if datos:
        df = frameDeDatos(datos, df)
        alfabeto = creaAlfabeto(df)
        print("Alfabeto: ",alfabeto)
        E = calcEntropia(df,alfabeto)
        print("Entropia:" ,E)
        print("longitud media: ",calcLong(df))
        if (Kraft(len(alfabeto), df)): 
            print("El codigo cumple con la inecuacion de Kraft")
            if inst(df): 
                print("El codigo es instantaneo") 
            else: 
                print("El codigo NO es instantaneo")
        else:
            print("El codigo no cumple con la inecuacion de Kraft")
        if compact(df, len(alfabeto)):
            print("El codigo es compacto") 
        else: 
            print("El codigo NO es compacto") 
     
    
def lecturaBin(filename): 
    try:
        archivo = open("Samples/" + filename)
        datos = archivo.read()
        data = datos.split(" ")        
        archivo.close()
        return data
    except FileNotFoundError: 
        print("El archivo" ,filename, "no existe") 
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
def calcEntropia(df, alfabeto): 
    base = len(alfabeto)
    E = 0
    for pro in df["probabilidad"]:
        E += (pro * ma.log(1/pro,base))
    return E

def calcLong(df): 
    prom = 0
    prom = (df["palabras"].str.len() * df["probabilidad"]).sum()
    return prom

def Kraft(r, df):
    kf = 0
    for word in df["palabras"]: 
        kf += (1/r)**len(word)
    print("kraft", kf)
    return (kf<=1)

def compact(df, r): 
    rep = 0
    for word in df["palabras"]: 
        if (len(word)> round(ma.log(1/df["probabilidad"][rep],r))): 
            return False
        rep += 1
    return True

def inst(df): 
   for i in range(len(df)):
    primer_dato = df.iloc[i, 0]
    for j in range(i + 1, len(df)):
        dato_consecuente = df.iloc[j, 0]
        if str(primer_dato).startswith(str(dato_consecuente)) or str(dato_consecuente).startswith(str(primer_dato)):
            return False
    return True

if __name__ == "__main__":
    main()