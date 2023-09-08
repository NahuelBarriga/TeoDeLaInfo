import random

# Definir la cantidad de unos y ceros que deseas generar
cantidad_unos = 50
cantidad_ceros = 50

# Generar una lista de unos y ceros aleatorios
datos = [random.choice([0, 1]) for _ in range(cantidad_unos + cantidad_ceros)]

# Definir el nombre del archivo binario

# Escribir los datos en el archivo binario
with open("Tp1/datos_binarios.bin", "wb") as archivo:
    archivo.write(bytes(datos))

print(f"Se ha generado")