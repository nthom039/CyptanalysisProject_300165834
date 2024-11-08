plaintext_ciphertext_right_pairs = []
with open('encryptionOutput/RightPairs.csv', 'r') as file:
    next(file)
    for line in file:
        line_data = line.split(',')
        # print(line_data)
        plaintext_ciphertext_right_pairs.append([line_data_item.strip() for line_data_item in line_data])

for i in plaintext_ciphertext_right_pairs:
    print(i)