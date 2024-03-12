import socket
import time
from threading import Thread
from threading import Lock
from queue import Queue

def wait_sec(seconds):
    for _ in range(seconds): 
        time.sleep(1)

def write_in_file(fout, addr, mess):
    # acquire the lock
    lock.acquire()
    
    try:
        # write in file
        fout.write(f"addr: {addr}, message: {mess}\n")
    
        # sleep
        wait_sec(3)
    
    finally:
        # relase the lock
        lock.release()

def start_client_thread(c, addr):
    print("got connection from", addr)

    # attach global variables
    global num_cons
    global ok
    global fout

    ok = False
    num_cons += 1

    # wait until there is less then 3 connections
    while num_cons < 3:
        pass

    # send and initial message
    c.send('Hello!'.encode())

    # recive message
    mess = c.recv(1024).decode()

    if lock.locked():
        # if it's locked then add to queue
        q.put((addr, mess))

        # wait unil locked
        while lock.locked():
            pass

        addr, mess = q.get()

        # write in file
        write_in_file(fout, addr, mess)
    else:
        # write in file
        write_in_file(fout, addr, mess)
    


    # close client
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

# create lock
lock = Lock()

# create queue
q = Queue()

# create global variables
num_cons = 0
ok = True

# open file
fout = open('out.txt', "w+")


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
