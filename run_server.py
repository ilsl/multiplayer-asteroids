import server

if __name__ == "__main__":
    running_server = server.Server(port=5555, server='')
    # Set the first Client to connect with an id of 0
    currentId = "0"
    # Get the object poitions of a server
    pos = running_server.build_object_pos()
    running_server.create_socket()
