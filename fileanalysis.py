import struct

def main():
    hexdump_file("code/common.dat", end = 0x300)
    extract_data_from_idx("code/common.idx")
    hexdump_file("saves/NEW HOPE.save", end = 0x300)

def hexdump_file(filepath, start = 0, end = 0, step = 48):
    with open(filepath, 'rb') as f:
        data = f.read()
    offset = start
    if end == 0 :
        end = len(data)
    print(f"==================== {filepath} ====================")
    while offset < end:
        chunk = data[offset : offset + step]
        hex_values = " ".join(f"{byte:02x}".replace("0", "-") for byte in chunk)
        ascii_values = "".join(chr(byte) if 32 <= byte <= 126 else " " for byte in chunk)
        print(f"{offset:08x}  {hex_values:<96} | {ascii_values} |")
        offset += step

def extract_data_from_idx(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    offset = 0
    
    offset += 3 # 00 02 01 "Signature"
    filecount, = struct.unpack('<Q', data[offset:offset+8])
    offset += 8
    for i in range(filecount) :
        s1, s2, s3, s4, s5 = struct.unpack('<IQQQ?', data[offset:offset+29])
        print(f"{i}: {s1} {s2} {s3} {s4} {s5}")
        offset += 29

if __name__ == "__main__" :
    main()