import socket
import time
from threading import Thread
import json
import sqlite3

def create_database(data: dict):
    global con

    cur = con.cursor()
    cur.execute(
        "CREATE TABLE persons(_ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT, TEL TEXT)"
    )
    con.commit()
    return 'done'

def query_database(data: dict):

    global con 

    cur = con.cursor()
    res = cur.execute(
        "SELECT * FROM persons"
    )

    return str(res.fetchall())

def insert_data(data: dict):
    global con

    cur = con.cursor()
    cur.execute(
        "INSERT INTO persons(name, tel) VALUES(?, ?)",
        (data['name'], data['tel'])
    )
    con.commit()
    return 'row inserted'

def insert_data(data: dict):
    global con

    cur = con.cursor()
    cur.execute(
        f"UPDATE persons SET name=?, tel=? WHERE _id={data['id']}",
        (data['name'], data['tel'])
    )
    con.commit()
    return 'row updated'

def delete_data(data: dict):
    global con

    cur = con.cursor()
    cur.execute(
        "DELETE FROM persons WHERE _id=?",
        (data['id'],)
    )
    con.commit()
    return 'row deleted'

def delete_database(data: dict):
    global con

    cur = con.cursor()
    cur.execute(
        "DROP TABLE persons"
    )
    con.commit()

    return 'database deleted'

functions = {
    'create_database': create_database,
    'query_database': query_database,
    'insert_data': insert_data,
    'delete_data': delete_data,
    'delete_database': delete_database
}

def start_client_thread(c, addr):
    print("got connection from", addr)

    global num_cons
    global ok

    ok = False
    num_cons += 1 

    # send and initial message
    c.send('1. Create Database\n2. Query Database\n3. Insert Data\n4. Update Data\n5. Delete Data\n6. Delete Database\n7. Exit(.)'.encode())

    # getting to loop
    while True:
        # recive message
        data_mess = c.recv(1024).decode()

        # check if data not None
        if data_mess != None:
            # check if it's end message
            if data_mess == 'end':
                break

            # decode data from json
            data = json.loads(data_mess)

            # find the function
            foo = functions[data['type']]

            # get the response from the database function
            ret = foo(data)
            
            # send back to client
            c.send(ret.encode())


    c.close()
    print("connection closed", addr)
    num_cons -= 1
    print("number of connections: ", num_cons)


if __name__ == '__main__':

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

    # create connection to database
    con = sqlite3.connect('database.db', check_same_thread=False)


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
