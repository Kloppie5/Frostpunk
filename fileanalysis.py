
def main():
    hexdump_file("code/common.dat")
    hexdump_file("code/common.idx")
    hexdump_file("saves/NEW HOPE.save")

def hexdump_file(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    offset = 0
    print(f"==================== {filepath} ====================")
    while offset < 1000:#len(data):
        chunk = data[offset : offset + 48]
        hex_values = " ".join(f"{byte:02x}".replace("0", "-") for byte in chunk)
        ascii_values = "".join(chr(byte) if 32 <= byte <= 126 else " " for byte in chunk)
        print(f"{offset:08x}  {hex_values:<96} | {ascii_values} |")
        offset += 48

if __name__ == "__main__" :
    main()