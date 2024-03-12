import socket
import time
from threading import Thread

def add(num1, num2):
    return num1 + num2

def sub(num1, num2):
    return num1 - num2

def mult(num1, num2):
    return num1 * num2

def div(num1, num2):
    return num1 // num2

def wait_sec(c, seconds):
    for _ in range(seconds): 
        c.send('.'.encode())
        time.sleep(1)

def start_client_thread(c, addr):
    print("got connection from", addr)

    global num_cons
    global ok
    ok = False
    num_cons += 1

    # send and initial message
    c.send('Operations: \n\tadd \n\tsub \n\tmult \n\tdiv \n\tend(.)\nType:\n\tint\n\tfloat'.encode())

    # getting to loop
    while True:
        # recive message
        data = c.recv(1024).decode()

        # check if data not None
        if data != None:
            # check if it's end message
            if data == 'end':
                break

            # get the operation and numbers
            type_str, op, num1, num2, time_str = data.split(',')
            if type_str == 'int':
                num1 = int(num1)
                num2 = int(num2)
            elif type_str == 'float':
                num1 = float(num1)
                num2 = float(num2)
            time_d = int(time_str)

            # choose the operation function
            foo = None
            if op == 'add':
                foo = add
            elif op == 'sub':
                foo = sub
            elif op == 'mult':
                foo = mult
            elif op == 'div':
                foo = div
            
            # check the function
            if foo != None:
                # wait for the server
                wait_sec(c, time_d)

                # do the function 
                res = foo(num1, num2)

                # send back the result
                c.send(str(res).encode())


    c.close()
    print("connection closed", addr)
    num_cons -= 1
    print("number of connections: ", num_cons)



# create socket
s = socket.socket()
print("socket created successfully")

# reserve a port
port = 12346

# bind the port
s.bind(('', port))
print(f"socket binded to {port}")

# 10 seconds timeout, for example
s.settimeout(1)  

# put the socket to listening
s.listen(1)
print("socket is listening")

num_cons = 0
ok = True

#while True:
while ok == True or num_cons > 0:
    try:
        # establish connection with the client
        c, addr = s.accept()

        # start a new thread
        Thread(target=start_client_thread, args=(c, addr, )).start()

        time.sleep(0.02)

        print("number of connections: ", num_cons)
    except:
        pass

s.close()
print('Server closed')
