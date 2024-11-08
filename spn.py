# S-box and its inverse
sbox = {0x0: 0xC, 0x1: 0x5, 0x2: 0xA, 0x3: 0x8, 0x4: 0x9, 0x5: 0xB, 0x6: 0xD, 0x7: 0x1, 0x8: 0x4, 0x9: 0x6, 0xA: 0xF, 0xB: 0xE, 0xC: 0x7, 0xD: 0x0, 0xE: 0x3, 0xF: 0x2}
sbox_inv = {0x0: 0xD, 0x1: 0x1, 0x2: 0xF, 0x3: 0xE, 0x4: 0x8, 0x5: 0x1, 0x6: 0x9, 0x7: 0xC, 0x8: 0x3, 0x9: 0x4, 0xA: 0x2, 0xB: 0x5, 0xC: 0x0, 0xD: 0x6, 0xE: 0xB, 0xF: 0xA}

# Permutation mapping
permutation = {0:0, 1:4, 2:8, 3:12, 4:1, 5:5, 6:9, 7:13, 8:2, 9:6, 10:10, 11:14, 12:3, 13:7, 14:11, 15:15}

# Keys for each round
keys = [0xB4B7, 0xD376, 0x083D, 0x26CF, 0x4D2C]

def encrypt(plaintext):
    currentCipher = plaintext
    for i in range(3):
        # Apply round key
        currentCipher = apply_key(currentCipher, i)
        # Apply S-box on each nibble
        currentCipher = apply_sbox(currentCipher)
        # Apply permutation
        currentCipher = apply_permutation(currentCipher)
    # Apply final round
    currentCipher = apply_key(currentCipher, 3)
    currentCipher = apply_sbox(currentCipher)
    # Apply final key
    currentCipher = apply_key(currentCipher, 4)
    return currentCipher

def apply_sbox(input):
    # Convert to 16-bit binary string
    input = format(input, '016b')
    output = 0
    for i in range(4):
        # convert to int, find sbox value and add to output value
        output += (sbox[int(input[4*i:4*(i+1)], 2)] << (3 - i) * 4)
    return output

def apply_key(plaintext, keyIndex):
    return plaintext ^ keys[keyIndex]

def apply_permutation(input):
    # Convert to 16-bit binary string
    input = format(input, '016b')
    output = ['0'] * 16
    # Apply permutation
    for i in range(16):
        output[permutation[i]] = input[i]
    # Convert back to integer
    return int(''.join(output), 2)

fileName = 'encryptionOutput/' + "Noah" + '.csv'
fd_w = open(fileName,"w+")
fd_w.write('Plaintext,Ciphertext\n')

for i in range(10000):
    ciphertext = encrypt(i)
    print(f"Plaintext: {hex(i)[2:].zfill(4)}, Ciphertext: {hex(ciphertext)[2:].zfill(4)}")
    fd_w.write(f"0x{hex(i)[2:].zfill(4)},0x{hex(ciphertext)[2:].zfill(4)}\n")

fd_w.close()