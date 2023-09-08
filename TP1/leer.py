#prueba de lectura

datos = []
with open("Tp1/datos_binarios.bin", "rb") as archivo:
    for byte in archivo.read(): 
        datos.append(byte)

print(datos[7])
