import sys

number = int(sys.argv[1])
number = 2 ** number

def fill_2_2(sq, c1, c2):
    sq[0][0] = c1
    sq[0][1] = c1
    sq[1][0] = c1

    sq[0][2] = c2
    sq[0][3] = c2
    sq[1][3] = c2

    sq[2][2] = c1
    sq[2][3] = c1
    sq[3][2] = c1

    sq[2][0] = c2
    sq[3][0] = c2
    sq[3][1] = c2
    
    return sq

def rotate(sq):
    leng = len(sq[0])
    for i in range(leng//2):
         for j in range(i, leng - i - 1):
            temp = sq[i][j]
            sq[i][j] = sq[leng -1 -j][i]
            sq[leng -1 -j][i] = sq[leng -1 -i][leng -1 -j]
            sq[leng -1 -i][leng -1 -j] = sq[j][leng -1 -i]
            sq[j][leng -1 -i] = temp

    return sq

def find_G(sq):

    number = len(sq)
    if sq[0][0] == "G":
        position = 0
    elif sq[0][number - 1] == "G":
        position = 3
    elif sq[number - 1][0] == "G":
        position = 1
    elif sq[number - 1][number - 1] == "G":
        position = 2
    else:
        position = 5

    return position

def break_table(sq):
    leng = len(sq[0])
    sq_1 = []
    sq_2 = []
    sq_3 = []
    sq_4 = []
    for i in range(leng//2):
        sq_1.append(sq[i][0 : leng//2])
        sq_2.append(sq[i][leng//2 : ])

    for i in range(leng//2, leng):
        sq_3.append(sq[i][0 : leng//2])
        sq_4.append(sq[i][leng//2 : ])

    number = len(sq_1)
    r = find_G(sq_1)
    if r == 5:
        sq_1[number//2][number//2] = "G"
        sq_1[number//2 -1][number//2] = "G"
        sq_1[number//2][number//2 -1] = "G"
    else:
        for i in range(r):    
            sq_1 = rotate(sq_1)
        sq_1[number//2][number//2] = "G"
        sq_1[number//2 -1][number//2] = "G"
        sq_1[number//2][number//2 -1] = "G"
        for i in range(4 - r):    
            sq_1 = rotate(sq_1)

    r = find_G(sq_2)
    for i in range(r):    
        sq_2 = rotate(sq_2)
    sq_2[number//2][number//2] = "G"
    sq_2[number//2 -1][number//2] = "G"
    sq_2[number//2][number//2 -1] = "G"
    for i in range(4 - r):    
        sq_2 = rotate(sq_2)

    r = find_G(sq_3)
    for i in range(r):    
        sq_3 = rotate(sq_3)
    sq_3[number//2][number//2] = "G"
    sq_3[number//2 -1][number//2] = "G"
    sq_3[number//2][number//2 -1] = "G"
    for i in range(4 - r):    
        sq_3 = rotate(sq_3)

    r = find_G(sq_4)
    for i in range(r):    
        sq_4 = rotate(sq_4)
    sq_4[number//2][number//2] = "G"
    sq_4[number//2 -1][number//2] = "G"
    sq_4[number//2][number//2 -1] = "G"
    for i in range(4 - r):    
        sq_4 = rotate(sq_4)

    return sq_1, sq_2, sq_3, sq_4

def loop(sq):
    sq_1, sq_2, sq_3, sq_4 = break_table(sq)

    number = len(sq_1)
    if number == 4:

        r = find_G(sq_1)
        if r == 5:
            for i in range(2):    
                sq_1 = rotate(sq_1)
            sq_1 = fill_2_2(sq_1, "B", "R")
            for i in range(2):    
                sq_1 = rotate(sq_1)
        else:
            for i in range(r + 2):    
                sq_1 = rotate(sq_1)
            sq_1 = fill_2_2(sq_1, "B", "R")
            for i in range(6 - r):    
                sq_1 = rotate(sq_1)

        r = find_G(sq_2)
        for i in range(r + 2):    
            sq_2 = rotate(sq_2)
        sq_2 = fill_2_2(sq_2, "R", "B")
        for i in range(6 - r):    
            sq_2 = rotate(sq_2)

        r = find_G(sq_3)
        for i in range(r + 2):    
            sq_3 = rotate(sq_3)
        sq_3 = fill_2_2(sq_3, "R", "B")
        for i in range(6 - r):    
            sq_3 = rotate(sq_3)

        r = find_G(sq_4)
        for i in range(r + 2):    
            sq_4 = rotate(sq_4)
        sq_4 = fill_2_2(sq_4, "B", "R")
        for i in range(6 - r):    
            sq_4 = rotate(sq_4)

    
    else:
        sq_1 = loop(sq_1)
        sq_2 = loop(sq_2)
        sq_3 = loop(sq_3)
        sq_4 = loop(sq_4)

    if len(sq_1) == 4:
        if sq_1[0][0] == "X":
            sq_1 = rotate(sq_1)
            sq_1 = rotate(sq_1)

    for i in range(number):
            sq_1[i] = sq_1[i] + sq_2[i]
            sq_3[i] = sq_3[i] + sq_4[i]
    
    sq = sq_1 + sq_3

    return sq

square = [["X" for col in range(number)] for row in range(number)]



if number == 2:
    square[0][0] = "G"
    square[1][0] = "G"
    square[1][1] = "G"

elif number == 4:
    square[number//2 -1][number//2 -1] = "G"
    square[number//2 -1][number//2] = "G"
    square[number//2][number//2 -1] = "G"
    
    square = fill_2_2(square, "B", "R")

else:
    square[number//2 -1][number//2] = "G"
    square[number//2][number//2 -1] = "G"
    square[number//2][number//2] = "G"

    square = loop(square)

for row in square:
    print(" ".join(map(str, row)))
