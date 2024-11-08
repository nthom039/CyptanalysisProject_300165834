# Load pairs from CSV and strip whitespace
plaintext_ciphertext_right_pairs = []
with open('encryptionOutput/Vekshan_RightPairs_0x0001.csv', 'r') as file:
    next(file)
    for line in file:
        line_data = line.split(',')
        plaintext_ciphertext_right_pairs.append([line_data_item.strip() for line_data_item in line_data])

# S-box and inverse S-box
sbox = {0x0: 0xC, 0x1: 0x5, 0x2: 0xA, 0x3: 0x8, 0x4: 0x9, 0x5: 0xB, 0x6: 0xD, 0x7: 0x1, 0x8: 0x4, 0x9: 0x6, 0xA: 0xF, 0xB: 0xE, 0xC: 0x7, 0xD: 0x0, 0xE: 0x3, 0xF: 0x2}
inv_sbox = {0x0: 0xD, 0x1: 0x7, 0x2: 0xF, 0x3: 0xE, 0x4: 0x8, 0x5: 0x1, 0x6: 0x9, 0x7: 0xC, 0x8: 0x3, 0x9: 0x4, 0xA: 0x2, 0xB: 0x5, 0xC: 0x0, 0xD: 0x6, 0xE: 0xB, 0xF: 0xA}



# Counter for key guesses
count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}

expected_zero_diff_positions = [0, 2, 3]  # Positions where the difference should be zero
expected_non_zero_diff_positions = [1]

def calculate_deltaC(ct1, ct2):
    return ct1 ^ ct2

# get single hex
def get_nibble(hex_value, nibble_position):
    return (hex_value >> (4 * (3 - nibble_position))) & 0xF

def is_possible_right_pair(ct1, ct2):
    deltaC = calculate_deltaC(ct1, ct2)
    
    # Check positions where difference should be zero
    for pos in expected_zero_diff_positions:
        if get_nibble(deltaC, pos) != 0:
            return False  # Discard pair if zero-difference positions are non-zero
    
    # Check positions where difference should be non-zero (if any are specified)
    for pos in expected_non_zero_diff_positions:
        if get_nibble(deltaC, pos) == 0:
            return False  # Discard pair if non-zero-difference positions are zero
    
    # Pair passes the filter criteria
    return True

def decrypt(ct1, ct2, delta_U4, pos):
    # deltaC = calculate_deltaC(ct1, ct2)

    # program does not like this
    # only use for generated right pairs
    # if(is_possible_right_pair(ct1, ct2) == False):
    #     return

    print(f"Analyzing Pair: C1={hex(ct1)}, C2={hex(ct2)}")
    # loop tru all posible subkeys
    for i in range(16):
        # Calculate inverted S-box output for the differential
        # inv_sbox_deltaC = inv_sbox[get_nibble(deltaC, pos) ^ i]
        inv_sbox_deltaC1 = inv_sbox[get_nibble(ct1, pos) ^ i]
        inv_sbox_deltac2 = inv_sbox[get_nibble(ct2, pos) ^ i]

        u = inv_sbox_deltaC1 ^ inv_sbox_deltac2
        
        # Check if this matches the expected differential nibble
        if u == get_nibble(delta_U4, pos):
            print(f"Found match at i = {hex(i)}")
            count[i] += 1

# Differential analysis on each pair
delta_U4 = 0x0200
pos = 1
for pair in plaintext_ciphertext_right_pairs:
    # print(pair)
    # print(f"Analyzing Pair: C1={pair[2]}, C2={pair[3]}")
    decrypt(int(pair[2], 16), int(pair[3], 16), delta_U4, pos)

print("Key guess counts:", count)
co = 0
for i in range(16):
    co += count[i]
print(co)

target = 9/256

print(target)
for i in range(16):
    # print("  ",target)
    # print(i, count[i]/len(plaintext_ciphertext_right_pairs))
    print(hex(i), count[i])
    # print(hex(i), count[i])
    # print("_______________________________________________")