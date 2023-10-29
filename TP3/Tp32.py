import sys
import os

def compress(original_file, compressed_file):
    with open("TP3/Samples/" + original_file , 'r') as f:
        data = f.read()

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

    with open("TP3/" + compressed_file, 'wb') as f:
        for i in result:
            f.write(i.to_bytes(2, byteorder='big'))

def decompress(compressed_file, decompressed_file):
    with open("TP3/" + compressed_file, 'rb') as f:
        data = f.read()

    dictionary = {i: chr(i) for i in range(256)}
    current_code = 256
    result = []

    current_str = ""
    for byte in data:
        current_code = (current_code << 8) + byte
        if current_code in dictionary:
            entry = dictionary[current_code]
        else:
            entry = current_str + current_str[0]

        result.append(entry)

        dictionary[current_code] = current_str + entry[0]
        current_code += 1

        current_str = entry

    with open(decompressed_file, 'w') as f:
        f.write(''.join(result))

def calculate_metrics(original_size, compressed_size):
    compression_ratio = original_size / compressed_size
    redundancy = 1 - compression_ratio
    performance = compressed_size / original_size

    return compression_ratio, redundancy, performance

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: tpi3 original.txt compressed.bin {-c|-d}")
        sys.exit(1)

    _, original_file, compressed_file, action = sys.argv

    if action == '-c':
        compress(original_file, compressed_file)
        print("Compresión completada.")
    elif action == '-d':
        decompress(compressed_file, original_file)
        print("Descompresión completada.")
    else:
        print("Acción no reconocida. Use -c para comprimir o -d para descomprimir.")
        sys.exit(1)

    original_size = os.path.getsize(original_file)
    compressed_size = os.path.getsize(compressed_file)

    compression_ratio, redundancy, performance = calculate_metrics(original_size, compressed_size)

    print("\nTasa de Compresión:", compression_ratio)
    print("Redundancia:", redundancy)
    print("Rendimiento:", performance)