class User:
    def __init__(self, name, client, addr):
        self.name = None
        self.client_socket = client
        self.addr = addr

    def set_name__(self, name):
        self.name = name

    def __repr__(self):
        return f"User_Info({self.addr}, {self.name})"

