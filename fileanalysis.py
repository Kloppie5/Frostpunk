from murmurhash2 import murmurhash2
import os
import struct
import zlib 

def main():
    extract_files()

def extend_filehashmap(hashmap, filepath):
    with open(filepath, "rb") as f:
        for line in f.read().split(b'\x00'):
            if line.startswith(b'\x01'):
                line = line[1:]
                hash = murmurhash2(line, 0)
                if hash not in hashmap :
                    print(f"New hash {hash}: {line.decode('utf8')}")
                    hashmap[hash] = line.decode('utf8')
            # line.rstrip('\x00')

def save_hashmap(hashmap, filepath):
    filenames = list(hashmap.values())
    filenames.sort()
    with open(filepath, "w") as f:
        f.writelines(line + '\n' for line in filenames)

def extract_files():
    hashmap = get_filehashmap("code/functionnames.txt")
    # extend_filehashmap(hashmap, f"extracted/unknown/60347917")
    save_hashmap(hashmap, "code/functionnames.txt")
    extract_files_from_dat(hashmap, "common")
    extract_files_from_dat(hashmap, "scenes")
    extract_files_from_dat(hashmap, "sequences")
    extract_files_from_dat(hashmap, "templates")
    # hexdump_file("saves/NEW HOPE.save", end = 0x300)


def get_filehashmap(filepath):
    hashmap = {}
    with open(filepath, 'r') as f:
        for line in f.readlines() :
            hash = murmurhash2(line[:-1].encode('utf8'), 0)
            hashmap[hash] = line[:-1]
    return hashmap

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

def extract_files_from_dat(hashmap, datatype):
    with open(f"code/{datatype}.dat", 'rb') as f:
        datdata = f.read()
    with open(f"code/{datatype}.idx", 'rb') as f:
        idxdata = f.read()

    idxoffset = 0
    idxoffset += 3 # 00 02 01 "Signature"
    filecount, = struct.unpack('<Q', idxdata[idxoffset:idxoffset+8])
    idxoffset += 8
    for i in range(filecount) :
        hash, datsize, decompressedsize, datoffset, s5 = struct.unpack('<IQQQ?', idxdata[idxoffset:idxoffset+29])
        
        if hash in hashmap :
            filepath = f"extracted/{datatype}/{hashmap[hash]}"
            unknown = False
        else :
            filepath = f"extracted/unknown/{hash}"
            unknown = True

        dat = datdata[datoffset:datoffset+datsize]
        decompressor = zlib.decompressobj(-zlib.MAX_WBITS)
        decompressed_data = decompressor.decompress(dat[10:])
        decompressed_data += decompressor.flush()
        dat = decompressed_data[:decompressedsize]

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(dat)
            if unknown :
                print(f"Unknown '{filepath}'")

        idxoffset += 29

if __name__ == "__main__" :
    main()