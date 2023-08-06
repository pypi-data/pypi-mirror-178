current_file = lambda: __file__
get_command_output = lambda command: __import__('subprocess').getoutput(command)
import socket

class my_ip:
    def __init__() -> (None):
        return socket.gethostbyaddr(socket.gethostname())
    def device_name() -> str:
        return socket.gethostname()
    


class Server:
    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))
        self.sock.listen(1)

    def accept_(self):
        return self.sock.accept()

    def close_(self):
        self.sock.close()

    def connect(self, host: str, port: int) -> None:
        try:
            self.sock.connect((host, port))
        except Exception as en:
            print(str(en))

class https:
    def __init__(self, url: str) -> None:
        self.req = __import__('requests').get(url)

    def statusCode(self) -> None:
        return self.req.status_code
    
    def getContent(self) -> None:
        return self.req.content
    

class Client:
    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', self.port))

    def send(self, data):
        self.sock.send(data)

    def recv(self, size):
        return self.sock.recv(size)

    def close(self):
        self.sock.close()

                
def get_conction(url) -> str:
    try:
        socket.create_connection((url, 80))
        return f"[{socket.gethostname()}]: Status: Online"
    except OSError:
        return f"[{socket.gethostname()}]: Status: Offline"