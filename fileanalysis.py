import zlib 
import struct

def main():
    extract_data_from_dat("code/common.dat", "code/common.idx")
    # hexdump_file("saves/NEW HOPE.save", end = 0x300)

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

def extract_data_from_dat(datfilepath, idxfilepath):
    with open(datfilepath, 'rb') as f:
        datdata = f.read()
    with open(idxfilepath, 'rb') as f:
        idxdata = f.read()

    idxoffset = 0
    idxoffset += 3 # 00 02 01 "Signature"
    filecount, = struct.unpack('<Q', idxdata[idxoffset:idxoffset+8])
    idxoffset += 8
    for i in range(filecount) :
        hash, datsize, decompressedsize, datoffset, s5 = struct.unpack('<IQQQ?', idxdata[idxoffset:idxoffset+29])
        dat = datdata[datoffset:datoffset+datsize]
        decompressor = zlib.decompressobj(-zlib.MAX_WBITS)
        decompressed_data = decompressor.decompress(dat[10:])
        decompressed_data += decompressor.flush()
        try:
            dat = decompressed_data[0:decompressedsize].decode('utf-8')
            print(f"{hash}: {dat}")
            with open(f"extracted/{hash}.lua", 'w') as f:
                f.write(dat)
        except:
            pass # textures, sounds, etc
        idxoffset += 29

if __name__ == "__main__" :
    main()