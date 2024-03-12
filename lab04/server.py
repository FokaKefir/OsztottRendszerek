import socket
import ntplib
from time import ctime

localIP = "127.0.0.1"
localPort = 20001

bufferSize = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Listen for incoming datagrams
while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    # Sending a reply to client
    response = ntplib.NTPClient().request('pool.ntp.org')
    bytesToSend = str.encode(ctime(response.tx_time))

    UDPServerSocket.sendto(bytesToSend, address)

    # get the message from the client
    msg, addr = UDPServerSocket.recvfrom(bufferSize)
    msg = msg.decode('utf-8')

    # do the summation
    strs = msg.split(' ')
    num1 = int(strs[0])
    num2 = int(strs[1])
    summation = num1 + num2

    # send the result
    res = str(summation)
    UDPServerSocket.sendto(res.encode('utf-8'), address)

