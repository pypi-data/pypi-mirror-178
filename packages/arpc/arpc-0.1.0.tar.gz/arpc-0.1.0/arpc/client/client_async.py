

import asyncio
import socket


BUFLEN = 1024


class ArpcConnAsync:

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

    async def handle_to(self, req_name: str, req_body: bytes) -> bytes:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, self.port))

        req_data = b''
        req_data += str(len(req_body)).encode()
        req_data += b'\n'
        req_data += req_name.encode()
        req_data += b'\n'
        req_data += req_body

        sock.sendall(req_data)
        sock.shutdown(socket.SHUT_WR)

        res_length = 0
        res_body = b''

        buf = sock.recv(BUFLEN)

        if res_length == 0:
            res = buf.split(b'\n')
            if len(res) > 2:
                res_length = int(res[0])
                res_body = res[2]
            else:
                pass

        sock.close()

        return res_body

    async def handle(self, req_name: str, req_body: bytes) -> bytes:
        reader, writer = await asyncio.open_connection(self.ip, self.port)

        req_data = b''
        req_data += str(len(req_body)).encode()
        req_data += b'\n'
        req_data += req_name.encode()
        req_data += b'\n'
        req_data += req_body

        writer.write(req_data)
        await writer.drain()

        res_length = 0
        res_body = b''

        buf = await reader.read(BUFLEN)

        if res_length == 0:
            res = buf.split(b'\n')
            if len(res) > 2:
                res_length = int(res[0])
                res_body = res[2]
            else:
                pass

        writer.close()
        await writer.wait_closed()

        return res_body


async def new_arpc_conn_async(ip: str, port: int) -> ArpcConnAsync:
    return ArpcConnAsync(ip, port)
