import json


class Base:

    def serialize(self):
        return json.dumps(self.__dict__).encode()

    @classmethod
    def deserialize(self, data):
        return self(**json.loads(data.decode()))

    def json(self):
        return self.__dict__


class BaseAsync:

    async def serialize(self):
        return json.dumps(self.__dict__).encode()

    @classmethod
    async def deserialize(self, data):
        return self(**json.loads(data.decode()))

    async def json(self):
        return self.__dict__
