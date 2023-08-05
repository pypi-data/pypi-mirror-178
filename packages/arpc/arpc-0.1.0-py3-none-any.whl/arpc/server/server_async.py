import asyncio
import sys


BUFLEN = 1024


class ServerAsync:

    def __init__(self, ip, port, client_count=8):
        self.handler = {}
        self.ip = ip
        self.port = port
        self.backlog = 128
        self.client_count = client_count

    async def register(self, name, func):
        self.handler[name] = func

    async def accept(self, reader, writer):
        length = 0
        name = ''
        body = b''

        buf = await reader.read(BUFLEN)

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
            writer.close()
            return

        res = await function(body, '')

        data = b''
        data += str(len(res)).encode()
        data += b'\n'
        data += name.encode()
        data += b'\n'
        data += res

        writer.write(data)
        await writer.drain()
        writer.close()

    async def _start(self):
        loop = asyncio.get_event_loop()
        
        try:
            import nest_asyncio
            nest_asyncio.apply()
        except Exception as e:
            print(e)

        coro = asyncio.start_server(self.accept, '127.0.0.1', 9000)
        server = loop.run_until_complete(coro)

        print('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            sys.exit(0)

        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

    async def start(self):
        await self._start()
