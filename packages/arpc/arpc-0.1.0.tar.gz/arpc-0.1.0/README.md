# arpc

> A framework of remote procedure call.

# Quick Start

#### arpc

```bash
# ${project}/arpc/api.arpc
arpc: 1.0

package {
    python: api
    go: api
}

procedures {
    procedure GetUserV1(RequestV1): ResponseV1
}

param RequestV1 {
    UserId: integer = 1
}

param ResponseV1 {
    UserId: integer = 1
    Username: string = 2
}
```

#### Compile

```bash
arpc -i ./arpc_file -o ./arpc_package -a true
```

#### Server

```python
from arpc.server import Server

from arpc_package.api.api import Arpc, RequestV1, ResponseV1


class S(Arpc):

    def get_user_v1(self, request: RequestV1) -> ResponseV1:
        print(request)
        return ResponseV1(user_id=1, username='arpc name')

    def post_user_v1(self, request: ResponseV1) -> RequestV1:
        print(request)
        return RequestV1(user_id=1)


def start():

    s = Server('127.0.0.1', 9000)

    c = S()
    c.register(s)

    s.start()


if __name__ == '__main__':
    start()
```

#### Server Async

> require package: nest-asyncio >= 1.5.6

```python
from arpc.server import ServerAsync

from arpc_package.api.api import Arpc, RequestV1, ResponseV1


class S(Arpc):

    async def get_user_v1(self, request: RequestV1) -> ResponseV1:
        print(request)
        return ResponseV1(user_id=1, username='arpc name')

    async def post_user_v1(self, request: ResponseV1) -> RequestV1:
        print(request)
        return RequestV1(user_id=1)


async def start():

    s = ServerAsync('127.0.0.1', 9000)

    c = S()
    await c.register(s)

    await s.start()


if __name__ == '__main__':
    asyncio.run(start_async())
```

#### Client

```python
import asyncio
from arpc.client import new_arpc_conn, new_arpc_conn_async
from arpc_package.api.api import Client, RequestV1


async def main_async():
    conn = await new_arpc_conn_async("127.0.0.1", 9000)
    client = Client(conn)
    request = RequestV1(user_id=1)
    response = await client.get_user_v1(request)
    print(await response.json())


def main():
    conn = new_arpc_conn("127.0.0.1", 9000)
    client = Client(conn)
    request = RequestV1(user_id=1)
    response = client.get_user_v1(request)
    print(response.json())


if __name__ == '__main__':
    # main()
    asyncio.run(main_async())
```
