import socket             
 
def error_message(mess):
    print(mess)

# create a socket object 
s = socket.socket()         
 
# define the port  
port = 12344        
 
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
        if inp == '.':
            send_to_server('end')
            break

        # split input
        lst = inp.split(" ")
        if len(lst) != 3:
            error_message("wrong operation")
        else:
            op_inp = lst[0]
            num1 = int(lst[1])
            num2 = int(lst[2])

            # find operation
            if op_inp == '+':
                op = "add"
            elif op_inp == '-':
                op = "sub"
            elif op_inp == '*':
                op = "mult"
            elif op_inp == '/':
                op = "div"
            else:
                error_message("wrong operation")
            
            # send message
            send_to_server(f"{op},{num1},{num2}")

            # recive the result
            res = s.recv(1024).decode()
            print(f"res: {res}")

    except:
        # exception
        error_message("error")

# close the connection 
s.close()     
print("connection closed")