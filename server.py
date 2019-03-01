import socket
from _thread import *
import json
from multiprocessing import Queue
import time


class Server:

    def __init__(self, port, server):
        self.port = port
        self.server = server

    def create_socket(self):
        """
        Create an INET, STREAMing socket and accept 2 threads
        :return: none
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # bind the socket to my local host, and a the port we defined in network.py
            s.bind((self.server, self.port))

        except socket.error as e:
            print(str(e))

        # become a server socket and accept 2 threads
        s.listen(2)
        print("Waiting for a connection")

        while True:
            conn, addr = s.accept()
            print("Connected to: ", addr)

            start_new_thread(self.threaded_client, (conn,))

    # The below initialises all objects on screen: Missile, Rock and ship.
    # This for loop creates a key specific to that rock. E.g rock 5 on screen would have a property of rockpositions_5
    def build_object_pos(self):
        """
        Create the dictionary of object positions
        :return: None
        """
        rockdict = {}
        for r in range(40):
            positionjson = "rocksposition_" + str(r)
            speedjson = "rockspeed_" + str(r)
            sizejson = "rocksize_" + str(r)
            directionjson = "rockdirection_" + str(r)
            jsonmessage = {positionjson: [67, 157], speedjson: 4, sizejson: 'big', directionjson: [0.2, 0.4]}
            rockdict = {**jsonmessage, **rockdict}

        missiledict = {}
        # This for loop creates a key specific to that missile. E.g rock 5 on screen would have a property of missilepositions_5
        for r in range(400):
            missileposition = "missileposition_" + str(r)
            missilespeed = "missilespeed_" + str(r)
            missiledirection = "missiledirection_" + str(r)
            jsonmissile = {missileposition: [67, 157], missilespeed: 4, missiledirection: [0.2, 0.4]}
            rockdict = {**jsonmissile, **missiledict}

        pos1 = {"id": 0, "position": [400.0, 300.0], 'angle': 0}
        pos2 = {"id": 1, "position": [100.0, 200.0], 'angle': 0}

        # Combine all of the dictionarys above
        pos1 = {**pos1, **rockdict}
        pos2 = {**pos2, **rockdict}

        pos = [pos1, pos2]
        return pos

    def threaded_client(self, conn):
        """
        Send the data received
        :return: dictionary
        """

        # Build queue
        queue = Queue()
        # Store up to 10 elements in the queue
        for i in range(10):
            queue.put(i)
        queue.put(None)  # Using None to indicate no more data on queue
        queue_active = True

        # Get the globally set currentId and pos
        global currentId, pos

        # send the serialized data across the network
        conn.send(str.encode(currentId))

        # This sets the 2nd Clients id
        currentId = "1"
        socket_active = True

        while True:
            # If there's nothing to read, bail out
            if not (socket_active or queue_active):
                break

            # By default, sleep at the end of the loop
            do_sleep = True
            try:
                data = conn.recv(4096)
                reply = data
                if not data:
                    # If no data has been received end the connection
                    conn.send(str.encode("Goodbye"))
                    break
                else:
                    # Decode the data received and load as json so we can check the id of the player
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
            # Get item from queue without blocking if possible
            if queue_active:
                try:
                    item = queue.get_nowait()
                    if item is None:  # Hit end of queue
                        queue_active = False
                    else:
                        do_sleep = False
                        self.process_queue_item(item)
                except Queue.Empty:
                    pass
            # If we didn't get anything on this loop, sleep for a bit so we
            # don't max out CPU time
            if do_sleep:
                time.sleep(0.1)

        print("Connection Closed")
        conn.close()

    def process_queue_item(self, item):
        print('Got queue item: %r' % item)


if __name__ == "__main__":
    running_server = Server(port=5555, server='')
    # Set the first Client to connect with an id of 0
    currentId = "0"
    # Get the object positions of a server`
    pos = running_server.build_object_pos()
    running_server.create_socket()
