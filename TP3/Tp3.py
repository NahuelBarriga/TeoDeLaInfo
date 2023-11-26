import sys
import os
import pandas as pd
from collections import Counter
import math as ma


def encode(data):
    diccionario = {chr(i): i for i in range(256)}
    ActCode = 256
    resultado = []
    strAct = ""
    for char in data:
        strAct += char
        if strAct not in diccionario: 
            resultado.append(diccionario[strAct[:-1]])
            diccionario[strAct] = ActCode
            ActCode += 1
            strAct = char

    if strAct in diccionario:
        resultado.append(diccionario[strAct])

    return resultado


def decode(data):
    # Descodifica un archivo de texto codificado con LZW.

    diccionario = {i: chr(i) for i in range(256)}
    ActCode = 256
    resultado = []
    previous_code = (data[1]) | (data[0]) << 8
    entry = diccionario[previous_code]
    resultado.append(diccionario[previous_code])  # inserta el primer caracter

    for i in range(2, len(data), 2):
        code = data[i + 1] | data[i] << 8
        if code in diccionario:
            current_entry = diccionario[code]
        elif code == ActCode:
            current_entry = entry + entry[0]

        resultado.append(current_entry)

        diccionario[ActCode] = entry + current_entry[0]
        ActCode += 1
        entry = current_entry

    return "".join(resultado)


def metricas(archOriginal, archCompress):
    df = pd.DataFrame(columns=["palabras", "apariciones", "probabilidad"])
    df = frameDeDatos(archCompress, df)
    E = calcDatos(df)
    original_size = os.path.getsize("Samples/" + archOriginal)
    compressed_size = os.path.getsize(archCompress)
    L = (
        compressed_size / original_size
    ) * 8  
    efi = E / L

    return  1 - (compressed_size / original_size), efi


def calcDatos(df):
    base = 2
    E = 0
    for pro in df["probabilidad"]:
        E += pro * ma.log(1 / pro, base)
    E = E / ma.log2(10)
    return E


def frameDeDatos(archCompress, df):
    data = []
    with open(archCompress, "rb") as f:
        data = f.read().hex()
    data = bytes.fromhex(data)
    array_de_hex = [int(data[i + 1] | data[i] << 8) for i in range(0, len(data), 2)]
    # print([int(array_de_hex[i]) for i in range(20)])
    diccionario = Counter(array_de_hex)
    tot = diccionario.total()
    for key in diccionario:
        col = {
            "palabras": key,
            "apariciones": diccionario[key],
            "probabilidad": diccionario[key] / tot,
        }
        df = df._append(col, ignore_index=True)
    return df


def main():
    args = sys.argv

    if len(args) != 4:
        print("Uso: tpi3 original.txt compressed.bin {-c|-d}")
        sys.exit(1)

    opcion = args[3]
    archOriginal = args[1]
    archCompress = args[2]

    if opcion == "-c":
        with open("Samples/" + archOriginal, "r") as f:
            data = str(f.read())
        encoded = encode(data)
        with open(archCompress, "wb") as f:
            for i in encoded:
                f.write(i.to_bytes(2, byteorder="big"))

        
        compRatio, efi = metricas(archOriginal, archCompress)

        print("Tasa de compresión: {:.2f}%".format(round(100 * compRatio, 2)))
        print("Eficiencia: {:.2f}%".format(round(100 * efi, 2)))
        print("Redundancia: {:.2f}%".format(round(100 * (1 - efi), 2)))
    elif opcion == "-d":
        with open(archCompress, "rb") as f:
            data = f.read().hex()

        data = bytes.fromhex(data)
        decoded = decode(data)
        with open(archOriginal, "w", encoding="utf-8") as f:
            f.write(decoded)


if __name__ == "__main__":
    main()
