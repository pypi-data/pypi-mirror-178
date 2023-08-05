from .snake_util import snake


def default(type_str):
    """
    This function is a template to generate default value.
    """
    if type_str == "int" or type_str == "integer":
        return "0"
    elif type_str == "float" or type_str == "double":
        return "0.0"
    elif type_str == "bool" or type_str == "boolean":
        return "False"
    elif type_str == "str" or type_str == "string":
        return "\"\""
    elif type_str == "list" or type_str == "array":
        return "[]"
    elif type_str == "dict" or type_str == "json" or type_str == "object":
        return "{}"
    else:
        return "None"


def generate_param_class(name, params, async_):
    """
    This function is a template to generate Param class.
    """

    params_list = []
    field_list = []

    for param in params:
        snake_name = snake(param['name'])
        params_list.append(snake_name)
        field_list.append(f"        self.{snake_name} = {snake_name}")

    if len(field_list) == 0:
        field_list.append("        pass")

    field_str = '\n'.join(field_list)

    template = f"""

class {name}({'BaseAsync' if async_ else 'Base'}):
    \"\"\"
    This class is a Param class for arpc.
    \"\"\"

    def __init__(self, {', '.join(params_list)}):
{field_str}
"""
    return template


def generate_procedure_class(_, unique, procedure, async_):
    """
    This function is a template to generate Procedure class.
    """
    async_ = "async " if async_ else ""
    await_ = "await " if async_ else ""
    await_s = ".serialize()" if async_ else ""

    package_id = unique

    strs_interface = []
    strs_client = []
    strs_server = []

    for p in procedure:
        snake_name = snake(p['name'])
        strs_interface.append(
            f"    @abc.abstractmethod\n    {async_}def {snake_name}(self, request: {p['request']}) -> {p['response']}: pass\n")
        strs_client.append(f"""
    {async_}def {snake_name}(self, request: {p['request']}) -> {p['response']}:
        data = {await_}request.serialize()
        res = {await_}self.conn.handle('{package_id}.{p['index']}', data)
        return {await_}{p['response']}.deserialize(res)""")
        if async_:
            strs_server.append(
                f"        await server.register('{package_id}.{p['index']}', await get_func(self.{snake_name}))")
        else:
            strs_server.append(
                f"        {await_}server.register('{package_id}.{p['index']}', lambda request, _: self.{snake_name}(\n            {p['request']}.deserialize(request)).serialize(){await_s})")

    interface_str = '\n'.join(strs_interface)
    client_str = '\n'.join(strs_client)
    server_str = '\n'.join(strs_server)

    inner_func = f"""
async def get_func(function):
    async def func(request, _):
        req = await RequestV1.deserialize(request)
        response = await function(req)
        return await response.serialize()
    return func

"""

    template = f"""
{inner_func if async_ else ''}
class Arpc(metaclass=abc.ABCMeta):
    \"\"\"
    This class is a Procedure class for arpc.
    \"\"\"

{interface_str}
    {async_}def register(self, server):
{server_str}


class Client:

    def __init__(self, conn):
        self.conn = conn
{client_str}


{async_}def new_client(conn):
    return Client(conn)
"""
    return template
