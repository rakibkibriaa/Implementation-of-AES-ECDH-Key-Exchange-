# first of all import the socket library 
import socket    
import importlib
import random
import math
main_file = importlib.import_module("1905098_f1")         


main_file.initialize_aes_sbox()

main_file.calcRoundConstant()

# next create a socket object 
s = socket.socket()         
print ("Socket successfully created")
 
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 12345   

factor = 2

key_size = 128


a = -1
b = -1

G_x = -1
G_y = -1

p = -1
 
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests 
# coming from other computers on the network 
s.bind(('', port))         
print ("socket binded to %s" %(port)) 
 
# put the socket into listening mode 
s.listen(5)     
print ("socket is listening")            
 
# a forever loop until we interrupt it or 
# an error occurs 
# Establish connection with client. 
c , addr = s.accept()     
print ('Got connection from', addr )

# send a thank you message to the client. encoding to send byte type. 
c.send('Thank you for connecting'.encode()) 
while True: 
 


  a = int(c.recv(4096).decode())
  c.send('ACK'.encode()) 

  b = int(c.recv(4096).decode())
  c.send('ACK'.encode()) 
  G_x = int(c.recv(4096).decode())
  c.send('ACK'.encode()) 
  G_y = int(c.recv(4096).decode('utf-8'))
  c.send('ACK'.encode()) 
  p = int(c.recv(4096).decode())
  c.send('ACK'.encode()) 

  aP_x = int(c.recv(4096).decode())
  c.send('ACK'.encode()) 

  aP_y = int(c.recv(4096).decode())
  c.send('ACK'.encode()) 

  E = int(p + 1 - 2 * math.sqrt(p))

  private =  random.randrange(2,E-1)

  point_x,point_y = main_file.compute_aP(private,G_x,G_y,a,p)   

  c.send(str(point_x).encode()) 
  c.recv(4096).decode()

  c.send(str(point_y).encode()) 
  c.recv(4096).decode()

  
  
  key_mine_x,key_mine_y = main_file.compute_aP(private,aP_x,aP_y,a,p)   

  #key_mine_x = 9012340001
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
          
  w = main_file.key_schedule(key_matrix)
  #print(key_matrix)
  # print(a)
  # print(b)
  # print(G_x)
  # print(G_y)
  # print(p)

  c.send('Ready'.encode())

  if(c.recv(4096).decode() == 'Ready'):

    received_msg = c.recv(4096).decode()

    c.send('ACK'.encode())

    received_hex_msg = ""

    for i in received_msg:

      a = hex(ord(i))

      diff = factor - len(a[2:])
      
      ss = ""
      for i in range(0,diff):
        ss = ss + '0'

      received_hex_msg = received_hex_msg + ss + a[2:]

      


    #print(received_hex_msg)
    cypher_list = []

    decypher_list = []

    total_blocks = len(received_hex_msg) * 4 // key_size

    for i in range(0,total_blocks):
      cypher_list.append(received_hex_msg[(i * key_size // 4) : (i * key_size // 4) + key_size // 4])

    
  
    ivv = cypher_list[0]

    decypher_list = []

    decypher_string = ""

    w = main_file.key_schedule(key_matrix)
    for i in range(1,len(cypher_list)): 

      decypher = main_file.AES_CBC_Decrypt(cypher_list[i],w,ivv)

      decypher_list.append(decypher)

      decypher_string = decypher_string + decypher

      ivv = cypher_list[i]


    #print(decypher_list)


    print('\n')
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
    if decypher_string.strip() == 'quit':
      c.close()
      break
    #print(ord(received_msg[0]))
    #for i in range(0,len(received_msg)):
      #received_msg[i] = hex(received_msg[i])

    #print(received_msg)
    # Close the connection with the client 
    #c.close()
    
    # Breaking once connection closed
    #break