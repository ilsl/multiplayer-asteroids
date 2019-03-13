# Don't run! Instead run the server.py

import server

if __name__ == "__main__":
    # Set the first Client to connect with an id of 0
    currentId = "0"
    running_server = server.Server(port=5555, server='', currentId=currentId)
    # Get the object positions of a server
    pos = running_server.build_object_pos()
    running_server.create_socket()
