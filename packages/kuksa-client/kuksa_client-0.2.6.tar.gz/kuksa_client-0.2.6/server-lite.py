import asyncio

import grpc.aio

from kuksa.val.v1 import val_pb2_grpc


class CallMock:
    def __init__(self):
        self._error = None  # to set gRPC status
        self.request = None
        self.response = None

    def __call__(self, request, context):
        self.request = request
        return self.response

"""
servicer_mock.Get.response = val_pb2.GetResponse(...)
assert (await client.get(...)) == [...]  # Abstract data types
assert servicer_mock.Get.request == val_pb2.GetRequest(...)
"""


"""
def servicer_mock_fixture(mocker):
    mocker.patch(val_pb2_grpc.VALServicer
"""

class VALTestServicer(val_pb2_grpc.VALServicer):
    def Get(self, request, context):
        self.servicer
        print(request)

    def Set(self, request, context):
        print(request)

    Subscribe = CallMock()

    def GetServerInfo(self, request, context):
        print(request)


async def amain():
    server = grpc.aio.server()
    servicer = VALTestServicer()
    servicer.Subscribe.response = []
    val_pb2_grpc.add_VALServicer_to_server(servicer, server)
    server.add_insecure_port('127.0.0.1:55555')
    forever = asyncio.Event()
    await server.start()
    try:
        await forever.wait()
    finally:
        await server.stop(grace=2.0)


def main():
    asyncio.run(amain())


if __name__ == '__main__':
    main()
