# S-box and its inverse
sbox = {0x0: 0xC, 0x1: 0x5, 0x2: 0xA, 0x3: 0x8, 0x4: 0x9, 0x5: 0xB, 0x6: 0xD, 0x7: 0x1, 0x8: 0x4, 0x9: 0x6, 0xA: 0xF, 0xB: 0xE, 0xC: 0x7, 0xD: 0x0, 0xE: 0x3, 0xF: 0x2}
sbox_inv = {0x0: 0xD, 0x1: 0x1, 0x2: 0xF, 0x3: 0xE, 0x4: 0x8, 0x5: 0x1, 0x6: 0x9, 0x7: 0xC, 0x8: 0x3, 0x9: 0x4, 0xA: 0x2, 0xB: 0x5, 0xC: 0x0, 0xD: 0x6, 0xE: 0xB, 0xF: 0xA}


# Permutation mapping
permutation = {0: 0, 1: 4, 2: 8, 3: 12, 4: 1, 5: 5, 6: 9, 7: 13, 8: 2, 9: 6, 10: 10, 11: 14, 12: 3, 13: 7, 14: 11, 15: 15}

# Keys for each round
keys = [0x36E7, 0xD568, 0xCDD2, 0x3141, 0xC1C2]

# Expected differences for differential characteristic
delta_P = 0x0001  

def encrypt(plaintext):
    currentCipher = plaintext
    for i in range(3):
        currentCipher = apply_key(currentCipher, i)
        currentCipher = apply_sbox(currentCipher)
        currentCipher = apply_permutation(currentCipher)
    currentCipher = apply_key(currentCipher, 3)
    currentCipher = apply_sbox(currentCipher)
    currentCipher = apply_key(currentCipher, 4)
    return currentCipher

def apply_sbox(input):
    input = format(input, '016b')
    output = 0
    for i in range(4):
        output += (sbox[int(input[4*i:4*(i+1)], 2)] << (3 - i) * 4)
    return output

def apply_key(plaintext, keyIndex):
    return plaintext ^ keys[keyIndex]

def apply_permutation(input):
    input = format(input, '016b')
    output = ['0'] * 16
    for i in range(16):
        output[permutation[i]] = input[i]
    return int(''.join(output), 2)

# Output file for right pairs
fileName = 'encryptionOutput/' + "Vekshan_RightPairs_inputDiff0x0001" + '.csv'
fd_w = open(fileName, "w+")
fd_w.write('Plaintext1,Plaintext2,Ciphertext1,Ciphertext2\n')

# Set to store unique pairs
unique_pairs = set()

# Generate and check for right pairs
for i in range(60000):
    P1 = i
    P2 = P1 ^ delta_P  # Generate P2 with the specified input difference
    
    # Create a sorted tuple of the plaintexts for uniqueness
    pair = tuple(sorted((P1, P2)))
    
    # Check if the pair is already in unique_pairs set
    if pair not in unique_pairs:
        C1 = encrypt(P1)
        C2 = encrypt(P2)

        # Add the pair to the set of unique pairs
        unique_pairs.add(pair)
        
        # Write the pair to the output file
        print(f"Right Pair - P1: {hex(P1)[2:].zfill(4)}, P2: {hex(P2)[2:].zfill(4)}, C1: {hex(C1)[2:].zfill(4)}, C2: {hex(C2)[2:].zfill(4)}")
        fd_w.write(f"0x{hex(P1)[2:].zfill(4)}, 0x{hex(P2)[2:].zfill(4)},0x{hex(C1)[2:].zfill(4)}, 0x{hex(C2)[2:].zfill(4)}\n")

fd_w.close()