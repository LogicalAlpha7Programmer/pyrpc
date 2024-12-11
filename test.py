import .pyrpc_server as pyrpc
def add(a, b):
    return a + b


def sub(a, b):
    return a - b


server = pyrpc.RPCServer()

server.registerMethod(add)
server.registerMethod(sub)

server.run()
