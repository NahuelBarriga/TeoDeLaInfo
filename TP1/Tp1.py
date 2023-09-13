import sys
import numpy as np

def main(): #!esto es temporal
    datos = [] 
    datos = lecturaBin()
    PMT,cuentaBin = armarMt(datos)
    #print(cuentaBin)
    print(PMT)
    calculoEntriopia(cuentaBin)


#    if len(sys.argv) < 2: 
#        print("cabecera de archivo invalida") 
#        return
#    else: 
#        filename = sys.argv[2] 
#        if (len(sys.argv)==3 and sys.argv[2] > 0):
#            N = int(sys.argv[2])
#        lecturaBin(filename)



#* Lectura de arch binario
def lecturaBin(): 
    datos = []
    try:
        with open("Tp1/Samples/tp1_sample2.bin", "rb") as archivo: #todo: agregar el sys.arg[2]
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

def calculoEntriopia(cuentaBin): 
    totS = sum(cuentaBin) 
    entropia = cuentaBin / totS
    print(entropia)
    return None


 
if __name__ == "__main__":
    main()