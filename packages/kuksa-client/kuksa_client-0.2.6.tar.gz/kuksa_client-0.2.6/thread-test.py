import time

import kuksa_client


config = {'protocol': 'grpc', 'address': '127.0.0.1', 'port': 55555, 'insecure': True}
client = kuksa_client.KuksaClientThread(config)
print("start")
client.start()
print("stop")
client.stop()
print("stopped")
client.join()
print("joined")
