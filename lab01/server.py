import socket

def add(num1, num2):
    return num1 + num2

def sub(num1, num2):
    return num1 - num2

def mult(num1, num2):
    return num1 * num2

def div(num1, num2):
    return num1 // num2

# create socket
s = socket.socket()
print("socket created successfully")

# reserve a port
port = 12344

# bind the port
s.bind(('', port))
print(f"socket binded to {port}")

# put the socket to listening
s.listen(1)
print("socket is listening")

# establish connection with the client
c, addr = s.accept()
print("got connection from", addr)

# send and initial message
c.send('Operations: \n\tadd(+) \n\tsub(-) \n\tmult(*) \n\tdiv(/) \n\tend(.)'.encode())

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
        op, num1, num2 = data.split(',')
        num1 = int(num1)
        num2 = int(num2)

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
            # do the function 
            res = foo(num1, num2)

            # send back the result
            c.send(str(res).encode())


c.close()
print("connection closed")
