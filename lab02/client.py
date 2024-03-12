import socket             
 
def error_message(mess):
    print(mess)

# create a socket object 
s = socket.socket()         
 
# define the port  
port = 12346

# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 
 
# receive data from the server and decoding to get the string.
print(s.recv(1024).decode())

def send_to_server(data):
    s.send(data.encode())

# get in loop
while True:

    # read from terminal
    inp = input(">")
    try:
        # check if it's end message
        if inp == '.' or inp == 'end':
            send_to_server('end')
            break

        # split input
        lst = inp.split(" ")
        if len(lst) != 5:
            error_message("not enough paramters")
        else:
            type_inp = lst[0]
            op_inp = lst[1]
            num1 = lst[2]
            num2 = lst[3]
            time_d = int(lst[4])

            # find operation
            if op_inp not in ['add', 'sub', 'mult', 'div']:
                error_message("wrong operation")
            else:
                op = op_inp

            if type_inp not in ['int', 'float']:
                error_message("wrong type")
            else:
                type_d = type_inp

            # send message
            send_to_server(f"{type_d},{op},{num1},{num2},{time_d}")

            mess = s.recv(1024).decode()
            while mess == '.':
                print(mess)
                mess = s.recv(1024).decode()

            # recive the result
            res = mess
            print(f"res: {res}")

    except NameError:
        # exception
        error_message("error")

# close the connection 
s.close()     
print("connection closed")