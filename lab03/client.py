import socket             
 
def error_message(mess):
    print(mess)

# create a socket object 
s = socket.socket()         
 
# define the port  
port = 12346

# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 

def send_to_server(data):
    s.send(data.encode())

# receive data from the server and decoding to get the string.
print(s.recv(1024).decode())


inp = input('Answer: ')
send_to_server(inp)

# close the connection 
s.close()     
print("connection closed")