import random
import time
import importlib

total_round = 11
sbox = [None] * 256

round_constant = []

dimension = 4

key_length = 128

factor = 2

main = importlib.import_module('1905098_f1')

main.initialize_aes_sbox()

main.calcRoundConstant()


#compute_aP(11,1,2) #x^3 + 2x + 2
#(b,c) =  compute_aP(18,5,1,2,17)

#print(b,c)
one_cell_size = factor * 4

division_factor = key_length // one_cell_size

key = input('Key:\n')

key_matrix = []
for i in key:
    key_matrix.append(hex(ord(i)))

diff = key_length // 4 - len(key)

for i in range(0,diff):
    key_matrix.append(hex(ord(' ')))

print('In ASCII: ' + key)
print('In HEX:', end=' ')
for i in key_matrix:
    print(i[2:], end=" ")

print('\n')

plain_text = input('Plain Text:\n')

plain_text_matrix = []
all_plain_text = []

count = 0
for i in plain_text:
    
    if(count % division_factor == 0 and count > 0):

        all_plain_text.append(plain_text_matrix)
        plain_text_matrix = []

    plain_text_matrix.append(hex(ord(i)))

    count = count + 1


if(len(plain_text) % division_factor != 0):

    plain_text_matrix = []

    ind = len(plain_text) // division_factor

    for i in range(ind * division_factor,len(plain_text)):
        plain_text_matrix.append(hex(ord(plain_text[i])))

    all_plain_text.append(plain_text_matrix)

else:
    all_plain_text.append(plain_text_matrix)


print('In ASCII: ' + plain_text)
print('In HEX: ', end=" ")


length = len(all_plain_text[len(all_plain_text) - 1])


padding_count = key_length//one_cell_size - length



for i in range(0,padding_count):
    all_plain_text[len(all_plain_text) - 1].append(hex(ord(' ')))

for i in range(0,len(all_plain_text)):
    for j in range(0,len(all_plain_text[i])):
        # if all_plain_text[i][j] == 0:
        #     print(format(i, '02d'))
        # else:
        a = all_plain_text[i][j]
        print(a[2:], end=" ")
    print(end = '\n')


arr_length = key_length//(factor * 4)

init_vector = ""

for i in range(0,arr_length):
    
    num = random.randint(0,pow(16,one_cell_size//4) - 1)

    a = hex(num)

    diff = factor - len(a[2:])
    ss = ""
    for k in range(0,diff):
        ss = ss + '0'
    ss = ss + a[2:]

    init_vector = init_vector + ss
   



cypher_string = init_vector
decypher_list = []


ivv = init_vector

full_cypher = ""

schedule_start_time = time.time() * 1000
w = main.key_schedule(key_matrix)
schedule_end_time = time.time() * 1000

encr_start_time = time.time() * 1000

for i in range(0,len(all_plain_text)):

    cypher = main.AES_CBC_Encrypt(all_plain_text[i],w,ivv)

    cypher_string = cypher_string + cypher


    ivv = cypher
    
encr_end_time = time.time() * 1000

ivv = init_vector

ascii_cypher_string = ""
for i in range(0,len(cypher_string) - 1,2):

    ascii = '0x' + cypher_string[i] + cypher_string[i + 1]
    #print(ascii)
    ascii_cypher_string = ascii_cypher_string + chr(int(ascii,16))


print('\nCiphered Text')
print('In Hex: ', end = ' ')
for i in range(0,len(cypher_string)-1,2):
    print(cypher_string[i],end="")
    print(cypher_string[i+1],end="")
    print(" ",end="")
    
print(end='\n')
print('In Ascii: '+ ascii_cypher_string)

received_msg = ascii_cypher_string

received_hex_msg = ""

for i in received_msg:

    a = hex(ord(i))

    diff = factor - len(a[2:])

    ss = ""
    for i in range(0,diff):
        ss = ss + '0'

    received_hex_msg = received_hex_msg + ss + a[2:]

cypher_list = []

decypher_list = []

total_blocks = len(received_hex_msg) * 4 // key_length

for i in range(0,total_blocks):
    cypher_list.append(received_hex_msg[(i * key_length // 4) : (i * key_length // 4) + key_length // 4])


ivv = cypher_list[0]

decypher_list = []

decypher_string = ""

dec_start_time = time.time() * 1000

for i in range(1,len(cypher_list)): 

    decypher = main.AES_CBC_Decrypt(cypher_list[i],w,ivv)

    decypher_list.append(decypher)

    decypher_string = decypher_string + decypher

    ivv = cypher_list[i]

dec_end_time = time.time() * 1000
#print(decypher_list)


print('Deciphered Text: ')
print('In Hex:',end=' ')

for i in range(0,len(decypher_string)):
    a = hex(ord(decypher_string[i]))
    diff = factor - len(a[2:])
    ss = ""
    for i in range(0,diff):
        ss = ss + '0'
    print(ss + a[2:],end=' ')


print("\nIn Ascii: ",end=' ')

print(decypher_string)



print('\nExecution Time Details: ')
print('Key Schedule Time: ', (schedule_end_time - schedule_start_time),'ms')
print('Encryption Time: ', (encr_end_time - encr_start_time),'ms')
print('Decryption Time: ', (dec_end_time - dec_start_time),'ms')