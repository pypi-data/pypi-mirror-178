import asyncio
import logging
import os

import grpc
import kuksa_pb2
import kuksa_pb2_grpc


async def run() -> None:
    # Business proxies will most likely not let your gRPC communication through and your client will hang.
    # Either use grpc.aio.insecure_channel's options param: options=(('grpc.enable_http_proxy', 0),) or unset your env
    # vars:
    try:
        del os.environ['http_proxy']
        del os.environ['https_proxy']
    except KeyError:
        pass
    # /!\ 'localhost' name resolution needs to work otherwise your client will hang.
    # async with grpc.aio.insecure_channel('127.0.0.1:55555') as channel:
    async with grpc.aio.insecure_channel('localhost:55555') as channel:
        print(channel.get_state())
        print("Waiting for channel to become ready")
        await channel.channel_ready()
        stub = kuksa_pb2_grpc.kuksa_grpc_ifStub(channel)
        print("Waiting for response")
        response = await stub.get(kuksa_pb2.GetRequest(type=kuksa_pb2.CURRENT_VALUE, path='Vehicle.Speed'))
    print(f"Kuksa client received: {response.values=}, {response.status=}")

    # TODO: Check TCP_USER_TIMEOUT configuration some day to figure out how to get fast feedback instead of hanging.


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
