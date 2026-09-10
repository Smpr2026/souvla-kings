#!/usr/bin/env python3
"""Crop a horizontal band out of a non-interlaced 8-bit PNG. usage: crop.py in.png out.png y height"""
import sys, zlib, struct

def read_png(path):
    d = open(path, 'rb').read()
    assert d[:8] == b'\x89PNG\r\n\x1a\n', 'not a png'
    pos, idat, hdr = 8, [], None
    while pos < len(d):
        ln = struct.unpack('>I', d[pos:pos+4])[0]
        typ = d[pos+4:pos+8]
        body = d[pos+8:pos+8+ln]
        if typ == b'IHDR': hdr = struct.unpack('>IIBBBBB', body)
        elif typ == b'IDAT': idat.append(body)
        elif typ == b'IEND': break
        pos += 12 + ln
    w, h, depth, ctype, comp, filt, inter = hdr
    assert depth == 8 and inter == 0, f'unsupported depth/interlace {depth}/{inter}'
    ch = {0:1, 2:3, 3:1, 4:2, 6:4}[ctype]
    raw = zlib.decompress(b''.join(idat))
    stride = w * ch
    rows, prev = [], bytearray(stride)
    p = 0
    for _ in range(h):
        f = raw[p]; p += 1
        line = bytearray(raw[p:p+stride]); p += stride
        if f == 1:
            for i in range(ch, stride): line[i] = (line[i] + line[i-ch]) & 255
        elif f == 2:
            for i in range(stride): line[i] = (line[i] + prev[i]) & 255
        elif f == 3:
            for i in range(stride):
                a = line[i-ch] if i >= ch else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
        elif f == 4:
            for i in range(stride):
                a = line[i-ch] if i >= ch else 0
                b = prev[i]; c = prev[i-ch] if i >= ch else 0
                pa, pb, pc = abs(b-c), abs(a-c), abs(a+b-2*c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        rows.append(bytes(line)); prev = line
    return w, h, ch, ctype, rows

def write_png(path, w, rows, ctype):
    raw = b''.join(b'\x00' + r for r in rows)
    def chunk(t, b): 
        c = struct.pack('>I', len(b)) + t + b
        return c + struct.pack('>I', zlib.crc32(t + b) & 0xffffffff)
    out = b'\x89PNG\r\n\x1a\n'
    out += chunk(b'IHDR', struct.pack('>IIBBBBB', w, len(rows), 8, ctype, 0, 0, 0))
    out += chunk(b'IDAT', zlib.compress(raw, 6))
    out += chunk(b'IEND', b'')
    open(path, 'wb').write(out)

src, dst, y, hh = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
x0 = int(sys.argv[5]) if len(sys.argv) > 5 else 0
ww = int(sys.argv[6]) if len(sys.argv) > 6 else None
w, h, ch, ctype, rows = read_png(src)
y = max(0, min(y, h - 1)); hh = min(hh, h - y)
band = rows[y:y+hh]
x0 = max(0, min(x0, w - 1)); ww = w - x0 if ww is None else min(ww, w - x0)
if x0 or ww != w:
    band = [r[x0*ch:(x0+ww)*ch] for r in band]
write_png(dst, ww, band, ctype)
print(f'{dst}  {ww}x{hh}  from x={x0} y={y} of {w}x{h}')
