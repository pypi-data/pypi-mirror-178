import socket
import threading


BUFLEN = 1024


class Server:

    def __init__(self, ip, port, client_count=8):
        self.handler = {}
        self.ip = ip
        self.port = port
        self.backlog = 128
        self.client_count = client_count

    def register(self, name, func):
        self.handler[name] = func

    def accept(self, client_socket):
        length = 0
        name = ''
        body = b''

        buf = client_socket.recv(BUFLEN)
        
        if length == 0:
            res = buf.split(b'\n')
            if len(res) > 2:
                length = int(res[0])
                name = res[1].decode()
                body = res[2]
            else:
                pass

        function = self.handler.get(name)
        if not function:
            print(f'not found handler {name}')
            client_socket.close()
            return

        res = function(body, '')

        data = b''
        data += str(len(res)).encode()
        data += b'\n'
        data += name.encode()
        data += b'\n'
        data += res

        client_socket.send(data)

        client_socket.close()

    def start(self):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, True)  # 设置端口复用
        tcp_socket.bind((self.ip, self.port))
        tcp_socket.listen(self.backlog)

        print(f'Serving on {self.ip}:{self.port}')
        try:
            while True:
                # 等待客户端连接
                client_socket, ip_port = tcp_socket.accept()
                t1 = threading.Thread(
                    target=self.accept, args=(client_socket,))
                t1.setDaemon(True)
                t1.start()
        except KeyboardInterrupt:
            pass
        finally:
            tcp_socket.close()
