import socket
import json

class Network:

    def __init__(self):
        # SOCK_STREAM is TCP
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1" # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
                                    # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
                                    # ipv4 address. This feild will be the same for all your clients.
        self.port = 5555
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        # Get the id of user either 0 or 1
        return self.client.recv(4096)

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(data)
            reply = self.client.recv(4096)
            return reply
        except socket.error as e:
            return str(e)
