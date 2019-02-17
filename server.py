import socket
from _thread import *
import json
import ast

# create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = ''
port = 5555

server_ip = socket.gethostbyname(server)

try:
    # bind the socket to my local host, and a the port we defined in network.py
    s.bind((server, port))

except socket.error as e:
    print(str(e))

# become a server socket
s.listen(2)
print("Waiting for a connection")

currentId = "0"
rockdict = {}
#for number of x rocks
for r in range(20):
    positionjson = "rocksposition_" + str(r)
    speedjson = "rockspeed_" + str(r)
    sizejson = "rocksize_" + str(r)
    directionjson = "rockdirection_" + str(r)
    jsonmessage = {positionjson: [67, 157], speedjson: 4, sizejson: 'big', directionjson: [0.2, 0.4]}
    rockdict = {**jsonmessage, **rockdict}

missiledict = {}
#for number of x rocks
for r in range(20):
    missileposition = "missileposition_" + str(r)
    missilespeed = "missilespeed_" + str(r)
    missiledirection = "missiledirection_" + str(r)
    jsonmissile = {missileposition: [67, 157], missilespeed: 4, missiledirection: [0.2, 0.4]}
    rockdict = {**jsonmissile, **missiledict}

pos1 = {"id": 0, "position": [400.0, 300.0], 'angle': 0}
pos2 = {"id": 1, "position": [100.0, 200.0], 'angle': 0}

pos1 = {**pos1, **rockdict}
pos2 = {**pos2, **rockdict}
print(pos1)
print(pos2)
pos = [pos1, pos2]

def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(4096)
            reply = data
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                dataid = reply.decode()
                dataid = json.loads(dataid)
                id = dataid['id']
                id = int(id[2])
                print('pos',pos)
                pos[id] = reply

                # Use the alternative id to the one received as this will be the other players response.
                if id == 0: reply = pos[1]
                if id == 1: reply = pos[0]

                if type(reply) == bytes:
                    reply =reply.decode("utf-8")
                reply = json.dumps(reply)
                reply = reply.encode()

            conn.sendall(reply)
        except:
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))



















