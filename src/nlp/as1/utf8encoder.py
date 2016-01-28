import sys
import array

def toBits(ipText):
    bits = bin(array.array('B', ipText)[0])
    bits = bits.replace('b', '')
    if(len(bits)>8):
        bits=bits[-8:]
    bits = '00000000'[len(bits):] + bits
    return bits

def toUTF8(ipChar):
    utf8Arr = []
    # convert to bits
    bitSeq1 = toBits(ipChar[0])
    bitSeq2 = toBits(ipChar[1])
    # 0 - 127         1 byte
    # 128 - 2047      2 byte
    # 2048 - 65535    3 byte
    # 65536 - 1114111 4 byte
    
    # input count
    number = int(bitSeq1 + bitSeq2, 2)
    numberBits = bitSeq1 + bitSeq2
    
    if 0 <= number <= 127:
        numBytes = 1
    elif 128 <= number <= 2047:
        numBytes = 2
    elif 2048 <= number <= 65535:
        numBytes = 3
    elif 65536 <= number <= 1114111:
        numBytes = 4
 
    if(numBytes > 1):
        # prepare MSBs
#         print numberBits
#         print number
        msb = ''
        for i in range(numBytes):
            msb += '1'
        msb = msb + '0'

        for i in range(numBytes - 1):
            # get 6 bits by 6 bits from the last
            last6Bits = numberBits[-6:]
            numberBits = numberBits[:-6]
            num = '10' + last6Bits
            utf8Arr.append(int(num, 2))
#             print num
        
        msb = msb + numberBits[-(8 - len(msb)):]
#         print msb
        utf8Arr.append(int(msb,2))
    else:
        #num of bytes required is one. straight conversion
        # convert bits to byte int
        utf8Arr.append(int(toBits(ipText[1]), 2))
        
    utf8Arr.reverse()
    return utf8Arr

print bin(225)
print bin(132)
print bin(134)
    
 
ipFile = sys.argv[1]
newFileBytes = []    
    
with open(ipFile, 'rb') as f:
    ipText = f.read(2)    
    while ipText:
        newFileBytes += toUTF8(ipText)
        ipText = f.read(2)
        
    f.close()

# Write binary data to a file
with open('utf8encoder_out.txt', 'wb') as f:
    f.write(bytearray(newFileBytes))
    f.close()
