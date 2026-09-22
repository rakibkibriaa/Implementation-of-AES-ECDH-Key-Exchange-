import random
import importlib
import math
import sympy.ntheory as nt
import time

main_file = importlib.import_module('1905098_f1')

total_round = 11
sbox = [None] * 256

round_constant = []

dimension = 4


key_length = key_size = 128

factor = 2

# G_x = 5
# G_y = 1


# a = -1

# b = -1

sum_B = sum_A = sum_key = 0


trials = 5

for i in range(0,trials):
    p = nt.randprime(2**(key_size - 1), 2**(key_size))

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

    start_time = time.time() * 1000
    point_x,point_y = main_file.compute_aP(private,G_x,G_y,a,p)
    end_time = time.time() * 1000

    sum_A = sum_A + (end_time - start_time)

    A = point_x


    private_other = random.randrange(2,E-1)
    start_time = time.time() * 1000
    point_x,point_y = main_file.compute_aP(private_other,G_x,G_y,a,p)
    end_time = time.time() * 1000

    sum_B = sum_B + (end_time - start_time)

    B = point_x

    start_time = time.time() * 1000

    shared_x,shared_y = main_file.compute_aP(private,point_x,point_y,a,p)

    end_time = time.time() * 1000

    sum_key = sum_key + (end_time - start_time)

    hex_key = hex(shared_x)

    hex_key = hex_key[2:]

    diff = key_size // 4 - len(hex_key)

    key_matrix = []

    temp = ""
    for i in range(0,diff):
        temp = temp + "0"

    hex_key = temp + hex_key



rows, cols = (3, 3)

li = [[0 for i in range(cols)] for j in range(rows)]

li[0][0] = sum_A/trials
li[0][1] = sum_B/trials
li[0][2] = sum_key/trials

key_size = 192

sum_B = sum_A = sum_key = 0

for i in range(0,trials):
    p = nt.randprime(2**(key_size - 1), 2**(key_size))

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

    start_time = time.time() * 1000
    point_x,point_y = main_file.compute_aP(private,G_x,G_y,a,p)
    end_time = time.time() * 1000

    sum_A = sum_A + (end_time - start_time)

    A = point_x


    private_other = random.randrange(2,E-1)
    start_time = time.time() * 1000
    point_x,point_y = main_file.compute_aP(private_other,G_x,G_y,a,p)
    end_time = time.time() * 1000

    sum_B = sum_B + (end_time - start_time)

    B = point_x

    start_time = time.time() * 1000

    shared_x,shared_y = main_file.compute_aP(private,point_x,point_y,a,p)

    end_time = time.time() * 1000

    sum_key = sum_key + (end_time - start_time)

    hex_key = hex(shared_x)

    hex_key = hex_key[2:]

    diff = key_size // 4 - len(hex_key)

    key_matrix = []

    temp = ""
    for i in range(0,diff):
        temp = temp + "0"

    hex_key = temp + hex_key




li[1][0] = sum_A/trials
li[1][1] = sum_B/trials
li[1][2] = sum_key/trials

key_size = 256

sum_B = sum_A = sum_key = 0

for i in range(0,trials):
    p = nt.randprime(2**(key_size - 1), 2**(key_size))

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

    start_time = time.time() * 1000
    point_x,point_y = main_file.compute_aP(private,G_x,G_y,a,p)
    end_time = time.time() * 1000

    sum_A = sum_A + (end_time - start_time)

    A = point_x


    private_other = random.randrange(2,E-1)
    start_time = time.time() * 1000
    point_x,point_y = main_file.compute_aP(private_other,G_x,G_y,a,p)
    end_time = time.time() * 1000

    sum_B = sum_B + (end_time - start_time)

    B = point_x

    start_time = time.time() * 1000

    shared_x,shared_y = main_file.compute_aP(private,point_x,point_y,a,p)

    end_time = time.time() * 1000

    sum_key = sum_key + (end_time - start_time)

    hex_key = hex(shared_x)

    hex_key = hex_key[2:]

    diff = key_size // 4 - len(hex_key)

    key_matrix = []

    temp = ""
    for i in range(0,diff):
        temp = temp + "0"

    hex_key = temp + hex_key
    



li[2][0] = sum_A/trials
li[2][1] = sum_B/trials
li[2][2] = sum_key/trials



print('\tComputation Time For')
print('K\tA\t\tB\t\tShared R')
for i in range(2,5):
    print(64 * i,end='\t')
    print(li[i - 2][0],end=' ms\t')
    print(li[i - 2][1],end=' ms\t')
    print(li[i - 2][2],end=' ms\t')
    print('\n')
