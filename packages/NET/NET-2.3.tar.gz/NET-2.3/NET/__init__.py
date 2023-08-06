import socket
import os



def current_file() -> None:
    try:
        return __file__
    except Exception as en:
        print(
            str(
                en
            )
        )

def get_command_output(command: str) -> str:
    try:
        return __import__('subprocess').getoutput(command)
    except Exception as en:
        print(
            str(
                en
            )
        )

class my_ip:
    def __init__() -> None:
        return socket.gethostbyaddr(socket.gethostname())
    def device_name() -> str:
        return socket.gethostname()
    
errorTab = [
    "{ port } Must Contain A Integer.",
    "{ host } Must Contain A String.",
    "{ url } Must Contain A String.",
    "{ max_connections } Must Contain A Integer."
]

class Server:
    def __init__(self, host, port, max_connections):
        if port is None:
            print(errorTab[0])
        if host is None:
            print(errorTab[1])
        if max_connections is None:
            print(errorTab[3])
        else:
            self.port = port
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((host, self.port))
            self.sock.listen(max_connections)

    def accept_(self):
        return self.sock.accept()

    def close_(self):
        self.sock.close()

    def connect(self, host: str, port: int) -> None:
        try:
            if host is None:
                print(errorTab[1])
            if port is None:
                print(errorTab[0])
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
    


class Client():
    def __init__(self, port):
        if port is None or '':
            try:
                return print(
                    errorTab[0]
                )
            except Exception as en:
                print(
                    en 
                )
        else: # lets try this now.
            try:
                self.sock = serv = socket.socket()
                serv.connect(('', port))
            except Exception as en:
                print(
                    en 
                )

    def send_data(self, data):
        self.sock.send(data)

    def recv_data(self, size):
        return self.sock.recv(size) 

    def close_connection(self):
        self.sock.close()

        # follow me 
def get_connection(url) -> str:
    try:
        if url is None:
            print(errorTab[2])
        else:
            socket.create_connection((url, 80))
            return f"[{socket.gethostname()}]: Status: Online"
    except OSError:
        return f"[{socket.gethostname()}]: Status: Offline"
    
class built_in:
    def __init__(self) -> None:
        print(
            str(
                "Please Use: { NET.built_in.server(host, port, max_connections) } -> str, int"
            )
        )

    def server(host:str,port:int,max_connection:int) -> None:
        try:
            Connections = max_connection
            Host = host
            Port = port
            online = False
            Server = socket.socket()
            online = True
            Server.bind((Host,Port))
            print("LocalHost | Powered By: NET (pkg: NET)")
            print()
            print("###########################################################")
            print(f"Server Status:                   Online: {online}")
            print(f"Port:                            {  {  Port  }  }")
            print(f"Link:                            https://localhost:{Port}")
            print(f"IP (Machine):                    {socket.gethostbyname(socket.gethostname())}")
            print(f"Name(Windows):                   {os.getlogin()}")
            print("Version:                         0.0.1(Default)")
            print(f"Max Connections                  { {Connections} }")
            print("###########################################################")
            Server.listen(Connections) 
            while True:
                client, addr = Server.accept()
                print(">", end=" ")
                con = input()
                client.send(con.encode())
        except Exception as en:
            print(
                str(
                    en
                )
            )
            with open("Log.txt", "w") as _file_:
                _file_.write(f"[ERR] -> {en}")
                _file_.close()

     
class about_NET:
    def __init__(self) -> None:
        try:
            f = open('about_NET', "r")
            read_file_content = f.read()
            print(read_file_content)
        except Exception or OSError as en:
            print(en)

