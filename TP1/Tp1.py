

#* Lectura de arch binario
datos = []
with open("Tp1/datos_binarios.bin", "rb") as archivo:
    for byte in archivo.read(): 
        datos.append(byte)


print(len(datos))