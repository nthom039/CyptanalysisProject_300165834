s_box = [0xC, 0x5, 0xA, 0x8, 0x9, 0xB, 0xD, 0x1, 0x4, 0x6, 0xF, 0xE, 0x7, 0x0, 0x3, 0x2]

ddt = []

for delta_x in range (0, 16):
    for target_delta_y in range(0, 16):
        count_deltaX_targetY = 0
        details = []
        
        for x1 in range(16):
            x2 = x1 ^ delta_x
            delta_y = s_box[x1] ^ s_box[x2]
            
            if delta_y == target_delta_y:
                count_deltaX_targetY += 1
                details.append(("x1=", x1, "x2=", x2, "s_box[x1]", s_box[x1], "s_box[x2]", s_box[x2], "delta_y", delta_y))
                
        ddt.append(count_deltaX_targetY)
        
for item_index in range(len(ddt)):
    if(item_index % 16 == 15):
        print(ddt[item_index])
        print(" " ,end='')
    else:
        print(ddt[item_index], "|", end='')