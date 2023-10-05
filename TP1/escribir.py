import numpy as np

numeros_binarios = np.zeros((8, 2))

for i in range(8):
    decimal = i
    binario = str(bin(i)[2:].zfill(3))  # Convierte el número en binario y asegura una longitud de 4 caracteres con ceros a la izquierda
    print((binario))
    numeros_binarios[i, 0] = str(decimal)
    numeros_binarios[i, 1] = str(binario)

print(numeros_binarios)
