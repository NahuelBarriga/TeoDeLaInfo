import sys

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
    """Descodifica un archivo de texto codificado con LZW."""

    dictionary = {i: chr(i) for i in range(256)}
    current_code = 256
    result = []
    entry = ""
    previous_code = data[0]

    result.append(dictionary[previous_code])

    for code in data[1:]:
        if code in dictionary:
            current_entry = dictionary[code]
        elif code == current_code:
            current_entry = entry + entry[0]
        else:
            raise ValueError("Bad compressed code")

        result.append(current_entry)

        dictionary[current_code] = entry + current_entry[0]
        current_code += 1
        entry = current_entry

    return "".join(result)


def main():
    args = sys.argv

    if len(args) != 4:
        print("Uso: tpi3 original.txt compressed.bin {-c|-d}")
        sys.exit(1)

    action = args[3]
    original_file = args[1]
    compressed_file = args[2]

    if action == "-c":
        with open("TP3/Samples/" + original_file, "r") as f:
            data = str(f.read())
        encoded = encode(data)
        with open("TP3/" + compressed_file, 'wb') as f:
            for i in encoded:
                f.write(i.to_bytes(2, byteorder='big'))

        #original_size = os.path.getsize(original_file)
        #compressed_size = os.path.getsize(compressed_file)

        #print("Tasa de compresión: {}%".format(100 * compressed_size / original_size))
    elif action == "-d":
        with open("TP3/" + compressed_file, "rb") as f:
            data = f.read()


        decoded = decode(data)
        print(len(decoded))
        with open("TP3/" + original_file, "w", encoding='utf-8') as f:
            f.write(decoded)

if __name__ == "__main__":
    main()
