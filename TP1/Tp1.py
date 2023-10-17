import sys
import numpy as np
import math as ma
#np.set_printoptions(precision=5, suppress=True) 

def custom_formatter(x):
    return f"'{x:0{N}str}'"  
np.set_printoptions(precision=5, suppress=True, formatter={'str': custom_formatter})


def main(): 
    if len(sys.argv) < 2: 
        print("cabecera de archivo invalida") 
    else: 
        filename = sys.argv[1] 
        if (len(sys.argv)==3):
            N = int(sys.argv[2])
        else: 
            N=0
        ejecuta(filename, N)
       


def ejecuta(filename, N): #!esto es temporal
    datos = [] 
    datos = lecturaBin(filename)
    if datos:
        PMT,cuentaBin = armarMt(datos)

        #print(cuentaBin)
        print("matriz de probabilidad condicional: ")
        print(PMT)
        E, prob = calculoEntropia(cuentaBin)
        print("probabilidades: ", prob)
        print("Entropia: ", E)
        if memoriaNoNull(PMT): 
            print("La fuente de memoria es nula")
            if (N>0): 
                prob, E = EntropiaN(prob, N)
                print("matriz de probabilidades: ")
                print(prob)
                print("Entropia de orden N: ", E)
        else:
            print("La fuente es de memoria no nula")
            print("Vector estacionario: ",calculoVEst(PMT))
        
#* Lectura de arch binario
def lecturaBin(filename): 
    datos = []
    try:
        with open("Samples/" + filename, "rb") as archivo: #todo: agregar el sys.arg[2]
            byte = archivo.read(1)
            while byte:
                for i in range(8):
                    datos.append((ord(byte) >> i) & 1)
                byte = archivo.read(1)
        return datos
    except FileNotFoundError: 
        print("El archivo" ,filename ,"no existe") 
        return None

def armarMt(datos):
    MT = np.zeros((2,2), dtype=int)
    cuentaBin = np.zeros(2) 
    act=datos[0]
    for pos in datos[1:]: 
        MT[pos,act] += 1 
        cuentaBin[act] += 1
        act=pos
    C0 = np.sum(MT[:,0])
    C1 = np.sum(MT[:,1]) 
    PMT = np.zeros((2,2))
    PMT[:,0] = (MT[:,0] / C0)
    PMT[:,1] = (MT[:,1] / C1)
    return PMT, cuentaBin

def calculoEntropia(cuentaBin): 
    totS = sum(cuentaBin) 
    prob = cuentaBin / totS
    entropia = 0
    for i in range(len(prob)): 
        entropia += prob[i]*ma.log2(1/prob[i])
    return entropia,prob

def EntropiaN(prob, N): 
    E = 0
    probN = np.zeros((2**N, 2))

    for i in range(probN.shape[0]): 
        posFis = i
        posStr = "{:0{width}b}".format(posFis, width=N)
        posBin = bin(posFis)[2:].zfill(N)
        probI = 1
        for j in range(len(posBin)):
            bit = int(posBin[j])
            probI *= prob[bit]
        probN[i,0] = posStr
        probN[i,1] = probI

    for i in range(probN.shape[0]): 
        E += probN[i,1] * ma.log2(1/probN[i,1])
    return probN, E

def memoriaNoNull(PMT): 
    if np.allclose(PMT[0,0], PMT[0,1], atol=0.02)  and  np.allclose(PMT[1,0], PMT[1,1], atol=0.02):
        return True
    else: 
        return False

def calculoVEst(PMT): 
    Ve = [1.0 / PMT.shape[0]] * PMT.shape[0]
    max_iteraciones = 100
    for _ in range(max_iteraciones):
        VeAnt = Ve.copy()
        Ve = [
            np.round(sum(PMT[i][j] * VeAnt[j] for j in range(PMT.shape[0])), decimals = 5)
            for i in range(PMT.shape[0])
        ]
        if np.allclose(Ve, VeAnt, atol = 1e-5):
            break
    return Ve

if __name__ == "__main__":
    main()

