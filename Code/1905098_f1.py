import numpy as np
import struct as st
from BitVector import BitVector
import random
import binascii
import time


total_round = 11
sbox = [None] * 256

round_constant = []

dimension = 4


key_length = 128

factor = 2

schedule_time_start = 0.0
schedule_time_end = 0.0


InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)



def calcRoundConstant():

    rc = 1
   
    for i in range(0,total_round):

        temp = []
        temp.append(rc)

        for j in range(0,dimension - 1):
            temp.append(0)


        if(rc < 0x80):
            rc = 2 * rc
        else:
            rc = (2 * rc) ^ (0x11B)
        
        round_constant.append(temp)
       


def getMatrix(key_matrix):
    arr = []
    temp = []
    for i in range (1,len(key_matrix)+1):
        temp.append(key_matrix[i - 1])
        if(i % 4 == 0):
           
            arr.append(temp)
            temp = []
    return arr


def circular_left_shift(arr):

    temp = []

    for i in arr:
        temp.append(i)

    temp.append(temp.pop(0))

    return temp

def subsByte(arr):
    ind = 0

    temp = []

    for i in arr:
        temp.append(i)

    for i in temp:
        temp[ind] = sbox[int(i, 0)]
        ind = ind + 1

   # print(temp)
    return temp
    


def ROTL8(x,shift):
    return np.uint8(x << shift) | np.uint8(x >> (8 - shift))



def initialize_aes_sbox():
    p = 1
    q = 1
    
    while True:
    
        p = (p ^ np.uint8(p << 1) ^ (0x1B if(p & 0x80) else 0))
      
        q = q ^ np.uint8(q << 1)
        q = q ^ np.uint8(q << 2)
        q = q ^ np.uint8(q << 4)


        q = q ^ (0x09 if(q & 0x80) else 0)

        xformed = q ^ ROTL8(q, 1) ^ ROTL8(q, 2) ^ ROTL8(q, 3) ^ ROTL8(q, 4)
        
        #print(xformed)
        sbox[p] = xformed ^ 0x63

    
        if(p == 1):
            break
    
    sbox[0] = 0x63


def addRoundConstant(arr,round):

    temp = []

    for i in arr:
        temp.append(i)

    for i in range(0,len(arr)):

        temp[i] = hex(temp[i] ^ round_constant[round][i])
    
    return temp


def g(arr,round):

    a = circular_left_shift(arr)

    
    a = subsByte(a)    

    a = addRoundConstant(a,round)

    return a


def xor_matrix(arr1,arr2):

    temp = []

    for i in range(0,len(arr1)):
        temp.append(hex(int(arr1[i],16) ^ int(arr2[i],16)))
    
    return temp


def key_schedule(key_matrix):

    
    w = getMatrix(key_matrix)



    for i in range(dimension,4*total_round):
        if(i % 4 == 0):
            w.append(xor_matrix(w[i - dimension] , g(w[i-1],i // 4 - 1)))
        elif(dimension > 6 and i % dimension == 4):
            w.append(xor_matrix(w[i - dimension] , subsByte(w[i - 1])))
        else:
            w.append(xor_matrix(w[i - dimension] , w[i - 1]))
    
    
    return w #((schedule_time_end - schedule_time_start) * 1000,w)

def Round(currRound,total_round,dimension,xor_mat,w):

    rows, cols = (dimension, dimension)

    #substitute bytes

    for i in range(0,dimension):
        for j in range(0,dimension):
            xor_mat[i][j] = hex(sbox[int(xor_mat[i][j],16)])


    #shift row

    shift_mat = [[0 for i in range(cols)] for j in range(rows)]

    for i in range(0,dimension):

        ind = 0
        for j in range(i,dimension):
            shift_mat[i][ind] = xor_mat[i][j]
            ind = ind + 1
        
        for j in range(0,i):
            shift_mat[i][ind] = xor_mat[i][j]
            ind = ind + 1

    mix_col_mat = [[0x0 for i in range(cols)] for j in range(rows)]

    temp_key = [[0 for i in range(cols)] for j in range(rows)]
    if(currRound != total_round - 1):
    #mix column

        mix_mat = [[0x02,0x03,0x01,0x01],[0x01,0x02,0x03,0x01],[0x01,0x01,0x02,0x03],[0x03,0x01,0x01,0x02]]

        for i in range(0,dimension):
        
            for j in range(0,dimension):
            
                for k in range(0,dimension):
                #result[i][j] += X[i][k] * Y[k][j]

                    a = BitVector(intVal  = int(mix_mat[i][k]), size = 16)

                    b = BitVector(intVal  = int(shift_mat[k][j],16), size = 16)
                    
                    modulus = BitVector(bitstring='100011011')
                    n = 8

                    c = a.gf_multiply_modular(b, modulus, n)

                    #print(c)
                    mix_col_mat[i][j] =  mix_col_mat[i][j] ^  int(c.get_bitvector_in_hex(),16)
                    

        for i in range(0,dimension):
            for j in range(0,dimension):
                mix_col_mat[i][j] = hex(mix_col_mat[i][j])

    else:
        for i in range(0,dimension):
            for j in range(0,dimension):
                mix_col_mat[i][j] = shift_mat[i][j]
    #print(mix_mat)
    #print(shift_mat)
    #print(mix_col_mat)

    state_matrix = [[0x0 for i in range(cols)] for j in range(rows)]

    
    i = 0
    for r in range(currRound*dimension,currRound*dimension + dimension):
        for j in range(0,dimension):
            temp_key[j][i] = w[r][j]
        i = i + 1


    for i in range(0,dimension):
        for j in range(0,dimension):
            state_matrix[i][j] = hex(int(temp_key[i][j],16) ^ int(mix_col_mat[i][j],16))


    #print(state_matrix)

    return state_matrix


def InvRound(currRound,total_round,dimension,xor_mat,w):

    rows, cols = (dimension, dimension)

    #substitute bytes

    # for i in range(0,dimension):
    #     for j in range(0,dimension):
    #         xor_mat[i][j] = hex(sbox[int(xor_mat[i][j],16)])

    temp_key = [[0 for i in range(cols)] for j in range(rows)]

    shift_mat = np.array(xor_mat)

    
    #inv shift row


    for i in range(0,dimension):
        shift_mat[i] = np.roll(shift_mat[i],i)

    
    #inv sub byte

    for i in range(0,dimension):
        for j in range(0,dimension):
            shift_mat[i][j] = hex(InvSbox[int(shift_mat[i][j],16)])
    
    #add round key
    i = 0
    for r in range(currRound*dimension,currRound*dimension + dimension):
        for j in range(0,dimension):
            temp_key[j][i] = w[r][j]
        i = i + 1
    
    if(currRound != 0):
        for i in range(0,dimension):
            for j in range(0,dimension):
                shift_mat[i][j] = hex(int(temp_key[i][j],16) ^ int(shift_mat[i][j],16))

    inv_mix_col_mat = [[0x0 for i in range(cols)] for j in range(rows)]

    if(currRound != 0):
    #mix column

        inv_mix_mat = [
                        [0x0e,0x0b,0x0d,0x09],
                        [0x09,0x0e,0x0b,0x0d],
                        [0x0d,0x09,0x0e,0x0b],
                        [0x0b,0x0d,0x09,0x0e]
                     ]

        for i in range(0,dimension):
        
            for j in range(0,dimension):
            
                for k in range(0,dimension):
                #result[i][j] += X[i][k] * Y[k][j]

                    a = BitVector(intVal  = int(inv_mix_mat[i][k]), size = 16)

                    b = BitVector(intVal  = int(shift_mat[k][j],16), size = 16)
                    
                    modulus = BitVector(bitstring='100011011')
                    n = 8

                    c = a.gf_multiply_modular(b, modulus, n)

                    #print(c)
                    inv_mix_col_mat[i][j] =  inv_mix_col_mat[i][j] ^  int(c.get_bitvector_in_hex(),16)
                    

        for i in range(0,dimension):
            for j in range(0,dimension):
                inv_mix_col_mat[i][j] = hex(inv_mix_col_mat[i][j])

    else:
        for i in range(0,dimension):
            for j in range(0,dimension):
                inv_mix_col_mat[i][j] = hex(int(temp_key[i][j],16) ^ int(shift_mat[i][j],16))
        

    return inv_mix_col_mat


def AES_CBC_Encrypt(plain_text_matrix,w,iv):


    iv_mat = []

    ind = 0
    for j in range(0,len(iv) // factor):
        a = ""
        for k in range(0,factor):
           
            a = a + iv[ind]
            ind = ind + 1
        iv_mat.append('0x' + a)
        
       
    #print('p',iv_mat)

    res_plain_text_matrix = []

   
    #print('plain_text_matrix',plain_text_matrix)
    
   
    for i in range(0,len(plain_text_matrix)):
       
       res_plain_text_matrix.append(hex(int(plain_text_matrix[i],16) ^ int(iv[i],16)))

    
    #print(res_plain_text_matrix)

    

    #w = key_schedule(key_matrix)



    #print('time',key_schedule_time)
    # for i in range(dimension,4*total_round):
    #     if(i % 4 == 0):
    #         w.append(xor_matrix(w[i - dimension] , g(w[i-1],i // 4 - 1)))
    #     elif(dimension > 6 and i % dimension == 4):
    #         w.append(xor_matrix(w[i - dimension] , subsByte(w[i - 1])))
    #     else:
    #         w.append(xor_matrix(w[i - dimension] , w[i - 1]))



    rows, cols = (dimension, dimension)
    temp_key = [[0 for i in range(cols)] for j in range(rows)]

    temp_plain = [[0 for i in range(cols)] for j in range(rows)]

    key_state_matrix = []



    ind = 0

    for i in range(0,dimension):
        for j in range(0,dimension):
            temp_key[j][i] = w[i][j]
            temp_plain[j][i] = res_plain_text_matrix[ind]
            ind = ind + 1


    #print('temp_key',temp_plain)
    xor_mat = [[0 for i in range(cols)] for j in range(rows)]

    for i in range(0,dimension):
        for j in range(0,dimension):
            xor_mat[i][j] = hex(int(temp_key[i][j], 16) ^ int(temp_plain[i][j], 16))


    #print(xor_mat)

    temp_arr = [[0 for i in range(cols)] for j in range(rows)]

    for i in range(0,dimension):
        for j in range(0,dimension):
            temp_arr[i][j] = xor_mat[i][j]

    #print('temp_arr',temp_arr)
        
    for i in range(1,total_round):
        temp_arr = Round(i,total_round,dimension,temp_arr,w)
    
    
    
    msg = ""

    for i in range(0,dimension):
        for j in range(0,dimension):
            a = temp_arr[j][i]

           
            #byte_string = bytes.fromhex('00' if a[2:] == '0' else  a[2:])        
                  
            diff = factor - len(a[2:])

            #print(diff)
            ss = ""
            for k in range(0,diff):
                ss = ss + '0'
            ss = ss + a[2:]

           
            msg = msg + ss

  
    return msg
    return temp_arr


def AES_CBC_Decrypt(cypher_text,w,iv):

    iv_mat = []

    ind = 0
    for j in range(0,len(iv) // factor):
        a = ""
        for k in range(0,factor):
           
            a = a + iv[ind]
            ind = ind + 1
        iv_mat.append('0x' + a)



    rows,cols = (dimension,dimension)

    cypher_text_matrix = [[0 for i in range(cols)] for j in range(rows)]

    ind = 0

    for i in range(0,dimension):

        for j in range(0,dimension):

            a = ""

            for k in range(0,factor):
                a = a + cypher_text[ind]
                ind = ind + 1

            cypher_text_matrix[j][i] = '0x' + a
    

   
   
    #w = key_schedule(key_matrix)


    temp_key = [[0 for i in range(cols)] for j in range(rows)]

    ind = 0



    for i in range(dimension * (total_round - 1),dimension * total_round):
        for j in range(0,dimension):
            
            temp_key[j][ind] = w[i][j]

        ind = ind + 1


    xor_mat = [[0 for i in range(cols)] for j in range(rows)]

    
    for i in range(0,dimension):
        for j in range(0,dimension):

            #print(int(temp_key[i][j], 16))
           #print(int(cypher_text_matrix[i][j], 16))

            #print(int(temp_key[i][j], 16) ^ int(cypher_text_matrix[i][j], 16))


            xor_mat[i][j] = hex(int(temp_key[i][j], 16) ^ int(cypher_text_matrix[i][j], 16))


    
    #print(xor_mat)
    for i in range(total_round - 2,-1,-1):
        xor_mat = InvRound(i,total_round,dimension,xor_mat,w)
    

    temp_mat = []
    for i in range(0,dimension):
        for j in range(0,dimension):
            temp_mat.append(xor_mat[j][i])

  
    res_plain_text_matrix = []


    #print('temp_mat',xor_mat)
    
    for i in range(0,len(temp_mat)):
       
     
      # print(int(iv[i],16))
      # print(int(temp_mat[i],16) ^ int(iv[i],16))
       res_plain_text_matrix.append(hex(int(temp_mat[i],16) ^ int(iv[i],16)))

  
    msg = ""



    for i in range(0,len(res_plain_text_matrix)):

        a = res_plain_text_matrix[i]

       
        
        byte_string = bytes.fromhex('00' if a[2:] == '0' else  a[2:])
        #byte_string = bytes.fromhex(a[2:])  
            
        msg = msg + byte_string.decode('utf-8')


    return msg


def hex_to_acii(hex_str):
    
    ind = 0
    msg = ""
    for i in range(0,len(hex_str) // factor):
        a = ""

        for j in range(0,factor):
            a = a + hex_str[ind]
            ind = ind + 1


        msg = msg + chr(int(a,16))


    return msg
    #print(ascii_str)

  
    #ascii = ascii_str.decode("utf-8")

   

def getBinary(a):

    temp = []
    while True:
        r = a % 2
        a = a // 2 

        temp.append(r)

        if a == 0:
            temp = temp[::-1]
            return temp


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def add(x1,y1,x2,y2,p,a):
    if (x1 == x2 and y1 == y2):
        temp_1 = (3 * (x1 ** 2) + a) % p
        temp_2 = modinv(2 * y1, p)

        s = (temp_1 * temp_2) % p

        #print(temp_2)
        

    else:
        temp_1 = (y2 - y1) % p
        temp_2 = modinv(x2 - x1, p)

        s = (temp_1 * temp_2) % p

    x3 =(s ** 2 -x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p

    return (x3,y3)


def compute_aP(a,x,y,A,prime):
    binary = getBinary(a)

    (p1,p2) = (None,None)

    t1 = x
    t2 = y

    init_x = x
    init_y = y
    for i in range(1,len(binary)):
        if binary[i] == 1:
            (x1, y1) =  add(t1,t2,t1,t2,prime,A)

            if x1 >= init_x:
                (p1,p2)  =  add(init_x,init_y,x1,y1,prime,A)
            else:
                (p1,p2)  =  add(x1,y1,init_x,init_y,prime,A)
            
        else:
            (p1, p2) =  add(t1,t2,t1,t2,prime,A)
        
        t1 = p1
        t2 = p2

    return (p1,p2)

def mem_s_i(i,x,p):
    return pow(x,(p-1)>>i,p) == 1

def tonelli_sqrt(c,p):
    if c%p ==0:
        return [0]
    
    if not mem_s_i(1,c,p):
        return []
    
    q = p-1

    ell = 0

    while q%2==0:
        ell = ell +1
        q = q//2

    while True:
        n = random.randrange(1,p)
        if not mem_s_i(1,n,p):
            break
    ninv = pow(n,p-2,p)

    e = 0

    for i in range(2,ell+1):
        if not mem_s_i(i,pow(ninv,e,p)*c,p):
            e = e +2**(i-1)

    a = pow(pow(ninv,e,p)*c,(q+1)//2,p)

    b = (pow(n,e//2,p)*a)%p
    
    return [b,p-b]

##################################################################################################################

# initialize_aes_sbox()

# calcRoundConstant()


# #compute_aP(11,1,2) #x^3 + 2x + 2
# #(b,c) =  compute_aP(18,5,1,2,17)

# #print(b,c)
# one_cell_size = factor * 4

# division_factor = key_length // one_cell_size

# key = input('Key:\n')

# key_matrix = []
# for i in key:
#     key_matrix.append(hex(ord(i)))

# print('In ASCII: ' + key)
# print('In HEX:')
# for i in key_matrix:
#     print(i[2:], end=" ")

# print('\n')

# plain_text = input('Plain Text:\n')

# plain_text_matrix = []
# all_plain_text = []

# count = 0
# for i in plain_text:
    
#     if(count % division_factor == 0 and count > 0):

#         all_plain_text.append(plain_text_matrix)
#         plain_text_matrix = []

#     plain_text_matrix.append(hex(ord(i)))

#     count = count + 1




# if(len(plain_text) % division_factor != 0):

#     plain_text_matrix = []

#     ind = len(plain_text) // division_factor

#     for i in range(ind * division_factor,len(plain_text)):
#         plain_text_matrix.append(hex(ord(plain_text[i])))

#     all_plain_text.append(plain_text_matrix)

# else:
#     all_plain_text.append(plain_text_matrix)







# print('In ASCII: ' + plain_text)
# print('In HEX:')




# length = len(all_plain_text[len(all_plain_text) - 1])


# padding_count = key_length//one_cell_size - length



# for i in range(0,padding_count):
#     all_plain_text[len(all_plain_text) - 1].append('0x00')

# for i in range(0,len(all_plain_text)):
#     for j in range(0,len(all_plain_text[i])):
#         # if all_plain_text[i][j] == 0:
#         #     print(format(i, '02d'))
#         # else:
#         a = all_plain_text[i][j]
#         print(a[2:], end=" ")
#     print(end = '\n')


# arr_length = key_length//(factor * 4)

# init_vector = ""

# for i in range(0,arr_length):
    
#     num = random.randint(0,pow(16,one_cell_size//4) - 1)

#     a = hex(num)

#     diff = factor - len(a[2:])
#     ss = ""
#     for k in range(0,diff):
#         ss = ss + '0'
#     ss = ss + a[2:]

#     init_vector = init_vector + ss
   






# cypher_list = []
# decypher_list = []


# ivv = init_vector

# full_cypher = ""

# for i in range(0,len(all_plain_text)):

#     cypher = AES_CBC_Encrypt(all_plain_text[i],key_matrix,ivv)

#     cypher_list.append(cypher)

    

#     ivv = cypher
    

# ivv = init_vector

# for i in range(0,len(cypher_list)):   
#     decypher = AES_CBC_Decrypt(cypher_list[i],key_matrix,ivv)
#     decypher_list.append(decypher)
#     ivv = cypher_list[i]




# msg = ""
# for i in decypher_list:
#     if i == '0x00':
#         continue
#     msg = msg + i
    

# print(msg)


