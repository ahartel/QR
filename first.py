import numpy as np
import matplotlib.pyplot as plt

def versionToDim(version):
    assert version == 1
    return 21

def versionToBytePos(version):
    assert version == 1
    dim = versionToDim(version)
    # The following dict contains the orientations and positions
    # of the data fields in the QR code for version 1
    fields = [('up', (slice(dim-6, dim-2), slice(dim-2, dim))),
              ('up', (slice(dim-10, dim-6), slice(dim-2, dim))),
              ('left', (slice(dim-12, dim-10), slice(dim-4, dim))),
              ('down', (slice(dim-10, dim-6), slice(dim-4, dim-2))),
              ('down', (slice(dim-6, dim-2), slice(dim-4, dim-2))),
              ('right', (slice(dim-2, dim), slice(dim-6, dim-2))),
              ('up', (slice(dim-6, dim-2), slice(dim-6, dim-4))),
              ('up', (slice(dim-10, dim-6), slice(dim-6, dim-4))),
              ('left', (slice(dim-12, dim-10), slice(dim-8, dim-4))),
              ('down', (slice(dim-10, dim-6), slice(dim-8, dim-6))),
              ('down', (slice(dim-6, dim-2), slice(dim-8, dim-6))),
              ('right', (slice(dim-2, dim), slice(dim-10, dim-6))),
              ]
    return fields

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

class Byte:
    def __init__(self, val):
        self.__val = val

    def __getitem__(self, num):
        return (self.__val>>num)&0x1

def encode_byte(byte, direction):
    if direction == 'up':
        ret = [[byte[7], byte[6]],
               [byte[5], byte[4]],
               [byte[3], byte[2]],
               [byte[1], byte[0]]]
        return ret
    elif direction == 'left':
        ret = [[byte[5], byte[4], byte[3], byte[2]],
               [byte[7], byte[6], byte[1], byte[0]]]
        return ret
    elif direction == 'down':
        ret = [[byte[1], byte[0]],
               [byte[3], byte[2]],
               [byte[5], byte[4]],
               [byte[7], byte[6]]]
        return ret
    elif direction == 'right':
        ret = [[byte[7], byte[6], byte[1], byte[0]],
               [byte[5], byte[4], byte[3], byte[2]]]
        return ret


def raw_data(version, string):
    dim = versionToDim(version)
    data = np.zeros((dim,dim), dtype=bool)
    pos = versionToBytePos(version)
    # encoding (alphanumeric)
    data[dim-1,dim-2] = True
    print len(string)
    data[pos[0][1]] = encode_byte(Byte(len(string)), direction=pos[0][0])
    
    for num, char in enumerate(string):
        data[pos[num+1][1]] = encode_byte(Byte(ord(char)),
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

def main():
    string = "Hello world"
    version = 1
    code = generateCode(string, version)

    plt.imshow(code, interpolation="none", cmap="Greys")
    plt.show()

main()
