from collections import namedtuple

Minutiae = namedtuple(
    'Minutiae',
    ['type', 'x', 'y', 'orientation', 'quality', 'label'],
    defaults=[None, None])

def load_iso19794(path: str):
    with open(path, 'rb') as f:
        t = f.read()
    magic = int.from_bytes(t[0: 4], 'big')
    version = int.from_bytes(t[4: 8], 'big')
    total_bytes = int.from_bytes(t[8: 12], 'big')
    im_w = int.from_bytes(t[14: 16], 'big')
    im_h = int.from_bytes(t[16: 18], 'big')
    resolution_x = int.from_bytes(t[18: 20], 'big')
    resolution_y = int.from_bytes(t[20: 22], 'big')
    f_count = int.from_bytes(t[22: 23], 'big')
    reserved_byte = int.from_bytes(t[23: 24], 'big')
    fingerprint_quality = int.from_bytes(t[26: 27], 'big')
    minutiae_num = int.from_bytes(t[27: 28], 'big')
    minutiaes = []
    for i in range(minutiae_num):
       x = 28 + 6 * i
       min_type = (t[x] >> 6) & 0x3
       min_x = int.from_bytes([t[x] & 0x3f, t[x+1]], 'big')
       min_y = int.from_bytes(t[x+2: x+4], 'big')
       angle = 360- t[x + 4]/255*360
       min_quality = t[x + 5]
       minutiaes.append(Minutiae(min_type, min_x, min_y, angle, min_quality))
    return minutiaes

minutiae = load_iso19794('1_1.ist')
print(minutiae)
