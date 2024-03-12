import socket
import time

got_4_times = 0
response_time = []
elapsed_time = []

msgFromClient = "Gib time UwU"
bytesToSend = str.encode(msgFromClient)

serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
while got_4_times != 4:
    start = time.time()

    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    end = time.time()

    cond = True

    while cond:
        start = start + (end - start) * 0.2

        if (abs(start - end) < 0.01):
            cond = False

    response_time.append(msgFromServer[0].decode("utf-8"))
    elapsed_time.append(end - start)

    # do the job
    inp = input("Enter two number: ")
    UDPClientSocket.sendto(inp.encode('utf-8'), serverAddressPort)

    # wait for the response
    res, addr = UDPClientSocket.recvfrom(bufferSize)
    print(res.decode('utf-8'))

    got_4_times += 1

print(response_time)
print(elapsed_time)

