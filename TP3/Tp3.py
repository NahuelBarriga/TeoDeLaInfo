import sys
import os

def encode(data):

    dictionary = {chr(i): i for i in range(256)}
    current_code = 256
    result = []
    current_str = ""
    for char in data:
        current_str += char
        if current_str not in dictionary:
            result.append(dictionary[current_str[:-1]])
            dictionary[current_str] = current_code
            current_code += 1
            current_str = char

    if current_str in dictionary:
        result.append(dictionary[current_str])
    
    return result


def decode(data):
    #Descodifica un archivo de texto codificado con LZW.

    dictionary = {i: chr(i) for i in range(256)}
    current_code = 256
    result = []
    previous_code = (data[1]) | (data[0]) << 8
    entry = dictionary[previous_code]
    result.append(dictionary[previous_code]) #inserta el primer caracter 

    for i in range(2, len(data), 2):
        code = data[i+1] | data[i] << 8
        if code in dictionary:
            current_entry = dictionary[code]
        elif code == current_code:
            current_entry = entry + entry[0]

            
        result.append(current_entry)

        dictionary[current_code] = entry + current_entry[0]
        current_code += 1
        entry = current_entry

    return "".join(result)

def metricas(original_file,compressed_file): 
    original_size = os.path.getsize("Samples/" + original_file)
    compressed_size = os.path.getsize(compressed_file)
    red = (original_size - compressed_size) / original_size
    return compressed_size / original_size, red


def main():
    args = sys.argv

    if len(args) != 4:
        print("Uso: tpi3 original.txt compressed.bin {-c|-d}")
        sys.exit(1)

    action = args[3]
    original_file = args[1]
    compressed_file = args[2]

    if action == "-c":
        with open("Samples/" + original_file, "r") as f:
            data = str(f.read())
        encoded = encode(data)
        with open(compressed_file, 'wb') as f:
            for i in encoded:
                f.write(i.to_bytes(2, byteorder='big'))

        compRatio,red = metricas(original_file,compressed_file)
    
        

        print("Tasa de compresión: {}%".format(100 * compRatio))
        print("Redundancia :", red)                                 #!no esta bien esto, que hay buscar bine como se hace
       
    elif action == "-d":
        with open(compressed_file, "rb") as f:
            data = f.read().hex()

        data = bytes.fromhex(data)

        decoded = decode(data)
        with open(original_file, "w", encoding='utf-8') as f:
            f.write(decoded)

if __name__ == "__main__":
    main()
