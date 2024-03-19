import socket 
import json            
 
def error_message(mess):
    print(mess)

def send_to_server(data):
    s.send(data.encode())

if __name__ == '__main__':

    # create a socket object 
    s = socket.socket()         
    
    # define the port  
    port = 12346

    # connect to the server on local computer 
    s.connect(('127.0.0.1', port)) 
    
    # receive data from the server and decoding to get the string.
    print(s.recv(1024).decode())

    # get in loop
    while True:

        # read from terminal
        inp = input("Choose option (1-7)>")
        try:
            # check if it's end message
            if inp == '.' or inp == 'Exit' or inp == '7':
                send_to_server('end')
                break

            data = dict()
            
            if inp == '1':
                data['type'] = 'create_database'
                mess = json.dumps(data)
                send_to_server(mess)
                
            elif inp == '2':
                data['type'] = 'query_database'
                mess = json.dumps(data)
                send_to_server(mess)
                
            elif inp == '3':
                data['type'] = 'insert_data'
                data['name'] = input("Enter name: ")
                data['tel'] = input("Enter tel.: ")
                mess = json.dumps(data)
                send_to_server(mess)

            elif inp == '4':
                data['type'] = 'update_data'
                data['id'] = int(input("Enter id: "))
                data['name'] = input("Enter name: ")
                data['tel'] = input("Enter tel.: ")
                mess = json.dumps(data)
                send_to_server(mess)

            elif inp == '5':
                data['type'] = 'delete_data'
                data['id'] = int(input("Enter id: "))
                mess = json.dumps(data)
                send_to_server(mess)

            elif inp == '6':
                data['type'] = 'delete_database'
                mess = json.dumps(data)
                send_to_server(mess)

            # recive message from server
            res = s.recv(1024).decode()

            print(f"res: {res}")

        except NameError:
            # exception
            error_message("error")

    # close the connection 
    s.close()     
    print("connection closed")