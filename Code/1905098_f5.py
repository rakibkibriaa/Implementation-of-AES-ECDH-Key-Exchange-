import socket            

import importlib

import random

import math

import sympy.ntheory as nt


main_file = importlib.import_module("1905098_f1")  

total_round = 11
sbox = [None] * 256

round_constant = []

dimension = 4


key_length = key_size = 128

factor = 2



###################################################################### 


main_file.initialize_aes_sbox()

main_file.calcRoundConstant()



one_cell_size = factor * 4

division_factor = key_length // one_cell_size


# Create a socket object 
s = socket.socket()         
 
# Define the port on which you want to connect 
port = 12345               
 
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 
 
# receive data from the server and decoding to get the string.

s.recv(1024).decode()

while True:

    
    
    G_x = 5
    G_y = 1


    a = -1

    b = -1

    p = nt.randprime(2**(key_length - 1), 2**(key_length))

    while True:
        a = random.randrange(0,100)
        b = random.randrange(0,100)

        if((4 * (a**3) + 27 * (b**2)) % p != 0):
            break


    G_x = -1
    G_y = -1
    while True:

        x = random.randrange(0,p)
        c = x**3 + a*x + b

        G_x = x

        ll = main_file.tonelli_sqrt(c,p)

        if(len(ll) != 0):
            G_y = ll[0]
            break



    E = int(p + 1 - 2 * math.sqrt(p))

    private =  random.randrange(2,E-1)

    point_x,point_y = main_file.compute_aP(private,G_x,G_y,a,p)   


    a = str(a).encode() 
    b = str(b).encode() 

    G_x = str(G_x).encode() 
    G_y = str(G_y).encode() 
    p = str(p).encode()  

    s.send(a)
    s.recv(1024).decode()
    s.send(b)
    s.recv(1024).decode()
    s.send(G_x)
    s.recv(1024).decode()
    s.send(G_y)
    s.recv(1024).decode()
    s.send(p)
    s.recv(1024).decode()
    s.send(str(point_x).encode())
    s.recv(1024).decode()
    s.send(str(point_y).encode())
    s.recv(1024).decode()


    private_other_x = int(s.recv(1024).decode())
    s.send('ACK'.encode())
    private_other_y = int(s.recv(1024).decode())
    s.send('ACK'.encode())

    #print(private_other)


    a = int(a.decode())
    p = int(p.decode())

    key_mine_x,key_mine_y = main_file.compute_aP(private,private_other_x,private_other_y,a,p)   

    hex_key = hex(key_mine_x)

    hex_key = hex_key[2:]

    diff = key_size // 4 - len(hex_key)

    key_matrix = []

    temp = ""
    for i in range(0,diff):
        temp = temp + "0"

    hex_key = temp + hex_key

    for i in range(0,len(hex_key) - 1,2):
        a = hex_key[i]
        a = a + hex_key[i + 1]
        key_matrix.append('0x' + a)
    
    #print(key_matrix)

    key_ascii = ""
    for i in key_matrix:
        key_ascii = key_ascii + chr(int(i,16))

    


    if(s.recv(1024).decode() == 'Ready'):
        
        s.send('Ready'.encode())
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
        print('In HEX:',end=' ')

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
        decypher_string = ""

        ivv = init_vector

    
        full_cypher = ""

        w = main_file.key_schedule(key_matrix)

        for i in range(0,len(all_plain_text)):

            cypher = main_file.AES_CBC_Encrypt(all_plain_text[i],w,ivv)

        
            cypher_string = cypher_string + cypher
            

            ivv = cypher
            

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

        s.send(ascii_cypher_string.encode())
        s.recv(1024).decode()

    

        if(plain_text == 'quit'):
            s.close() 
            break


    
     