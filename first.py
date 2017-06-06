import numpy as np
import matplotlib.pyplot as plt

def versionToDim(version):
    assert version == 1
    return 21

def versionToBytePos(version):
    assert version == 1
    dim = versionToDim(version)
    return [('up', (slice(dim-6,dim-2), slice(dim-2,dim))),
            ('up', (slice(dim-10,dim-6), slice(dim-2,dim))),
            ('left', (slice(dim-12,dim-10), slice(dim-4,dim))),
            ]

def emptyCode(version):
    dim = versionToDim(version)
    empty = np.zeros((dim,dim), dtype=bool)

    return empty
    
def cornerMask(version):
    dim = versionToDim(version)
    corners = np.zeros((dim,dim), dtype=bool)
    for offset_x, offset_y in [(0,0), (dim-7,0), (0,dim-7)]:
        # upper bar of square
        corners[offset_y+0,offset_x+0:offset_x+6] = True
        # lower bar of square
        corners[offset_y+6,offset_x+0:offset_x+7] = True
        # left bar of square
        corners[offset_y+0:offset_y+6,offset_x+0] = True
        # right bar of square
        corners[offset_y+0:offset_y+6,offset_x+6] = True
        # inner square
        corners[offset_y+2,offset_x+2:offset_x+5] = True
        corners[offset_y+3,offset_x+2:offset_x+5] = True
        corners[offset_y+4,offset_x+2:offset_x+5] = True

    return corners

def fixedPattern(version):
    dim = versionToDim(version)
    pattern = np.zeros((dim,dim), dtype=bool)
    pattern[6,8:dim-8:2] = True
    pattern[8:dim-8:2,6] = True
    return pattern

def encode_byte(int, direction):
    if direction == 'up':
        ret = np.zeros((4,2))
        ret[3,1] = (int>>0)&0x1
        ret[3,0] = (int>>1)&0x1
        ret[2,1] = (int>>2)&0x1
        ret[2,0] = (int>>3)&0x1
        ret[1,1] = (int>>4)&0x1
        ret[1,0] = (int>>5)&0x1
        ret[0,1] = (int>>6)&0x1
        ret[0,0] = (int>>7)&0x1
        return ret
    elif direction == 'left':
        ret = np.zeros((2,4))
        ret[1,3] = (int>>0)&0x1
        ret[1,2] = (int>>1)&0x1
        ret[0,3] = (int>>2)&0x1
        ret[0,2] = (int>>3)&0x1
        ret[0,1] = (int>>4)&0x1
        ret[0,0] = (int>>5)&0x1
        ret[1,1] = (int>>6)&0x1
        ret[1,0] = (int>>7)&0x1
        return ret


def raw_data(version, string):
    dim = versionToDim(version)
    data = np.zeros((dim,dim), dtype=bool)
    pos = versionToBytePos(version)
    # encoding (alphanumeric)
    data[dim-1,dim-2] = True
    print len(string)
    data[pos[0][1]] = encode_byte(len(string), direction=pos[0][0])
    
    for num, char in enumerate(string):
        data[pos[num+1][1]] = encode_byte(ord(char),
                                          direction=pos[num+1][0])

    return data

def generateCode(string, version):
    empty = emptyCode(version)
    corners = cornerMask(version)
    fixed = fixedPattern(version)
    data = raw_data(version, string)

    merged = np.logical_or(empty, corners)
    merged = np.logical_or(merged, fixed)
    merged = np.logical_or(merged, data)
    return merged

if __name__ == '__main__':
    string = "He"
    version = 1
    code = generateCode(string, version)

    plt.imshow(code, interpolation="none", cmap="Greys")
    plt.show()
