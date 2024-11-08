plaintext_ciphertext = []
with open('encryptionOutput/Vekshan.csv', 'r') as file:
    next(file)
    for line in file:
        line_data = line.split(',')
        # print(line_data)
        plaintext_ciphertext.append([line_data_item.strip() for line_data_item in line_data])

right_pairs = []

deltaP = 0x0007

used_plaintexts_as_plaintext2 = set()

def is_right_pair(plaintext1, plaintext2, ciphertext1, ciphertext2):
    return (plaintext1, ciphertext1) != (plaintext2, ciphertext2) and int(plaintext1, 16) ^ int(plaintext2, 16) == deltaP

# Loop through plaintext_ciphertext list and find right pairs
for i in range(len(plaintext_ciphertext)):
    for j in range(i + 1, len(plaintext_ciphertext)):
        # Unpack the pairs for readability (assuming structure: [plaintext, ciphertext])
        plaintext1, ciphertext1 = plaintext_ciphertext[i]
        plaintext2, ciphertext2 = plaintext_ciphertext[j]
        
        # Check if they meet the right pair condition and if plaintext2 has not been used as a previous plaintext1
        if is_right_pair(plaintext1, plaintext2, ciphertext1, ciphertext2) and plaintext2 not in used_plaintexts_as_plaintext2:
            right_pairs.append((plaintext1, ciphertext1, plaintext2, ciphertext2))
            used_plaintexts_as_plaintext2.add(plaintext2)
            print(plaintext1, ciphertext1, plaintext2, ciphertext2)

fileName = 'encryptionOutput/' + "Vekshan_RightPairs_0x0007" + '.csv'
fd_w = open(fileName, "w+")
fd_w.write('Plaintext1,Plaintext2,Ciphertext1,Ciphertext2\n')

# Output the right pairs to verify
for pair in right_pairs:
    print(pair)
    fd_w.write(f"{(pair[0])},{pair[2]},{pair[1]},{pair[3]}\n")

fd_w.close()