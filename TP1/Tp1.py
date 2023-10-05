import sys
import numpy as np
import math as ma
np.set_printoptions(precision=5, suppress=True)
N = 3 #!sacar

#    if len(sys.argv) < 2: 
#        print("cabecera de archivo invalida") 
#        return
#    else: 
#        filename = sys.argv[2] 
#        if (len(sys.argv)==3 and sys.argv[2] > 0):
#            N = int(sys.argv[2])
#        lecturaBin(filename)

def main(): #!esto es temporal
    datos = [] 
    datos = lecturaBin()
    PMT,cuentaBin = armarMt(datos)
    #print(cuentaBin)
    print("matriz de probabilidad condicional: ")
    print(PMT)
    E, prob = calculoEntropia(cuentaBin)
    print("probabilidades: ", prob)
    print("Entropia: ", E)
    if memoriaNoNull(PMT): 
        prob, E = EntropiaN(prob, N)
        print("matriz de probabilidades: ")
        print(prob)
        print("Entropia de orden N: ", E)


    else:
        print("La fuente es de memoria no nula")
        calculoVEst(PMT)
        
#* Lectura de arch binario
def lecturaBin(): 
    datos = []
    try:
        with open("Tp1/Samples/tp1_sample6.bin", "rb") as archivo: #todo: agregar el sys.arg[2]
            byte = archivo.read(1)
            while byte:
                for i in range(8):
                    datos.append((ord(byte) >> i) & 1)
                byte = archivo.read(1)
        return datos
    except FileNotFoundError: 
        print("El archivo {filename} no existe") 
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
        i2 = i
        posBin = bin(posFis)[2:].zfill(N)
        posFis = bin(i2)[2:].zfill(N)
        probI = 1
        for j in range(len(posBin)):
            bit = int(posBin[j])
            probI *= prob[bit]
        probN[i,0] = (posFis)
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
    
    return None

 
if __name__ == "__main__":
    main()