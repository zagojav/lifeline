import struct
import sys

def build_ico(png_paths, out_path):
    images = []
    for p in png_paths:
        with open(p, "rb") as f:
            data = f.read()
        # read width/height from PNG IHDR (bytes 16-24)
        w, h = struct.unpack(">II", data[16:24])
        images.append((w, h, data))

    header = struct.pack("<HHH", 0, 1, len(images))
    entries = b""
    offset = 6 + 16 * len(images)
    body = b""
    for w, h, data in images:
        w_byte = 0 if w >= 256 else w
        h_byte = 0 if h >= 256 else h
        entries += struct.pack(
            "<BBBBHHII", w_byte, h_byte, 0, 0, 1, 32, len(data), offset
        )
        body += data
        offset += len(data)

    with open(out_path, "wb") as f:
        f.write(header + entries + body)

if __name__ == "__main__":
    out = sys.argv[1]
    pngs = sys.argv[2:]
    build_ico(pngs, out)
    print(f"wrote {out} from {pngs}")
