import logging
import logging.config

logging.config.fileConfig('kuksa_client/logging.ini')

import kuksa_client.grpc
from kuksa_client.grpc import Datapoint

with kuksa_client.grpc.VSSClient('127.0.0.1', 55555) as client:
    print("Before:", client.get_current_values(('Vehicle.Speed',)))
    client.set_current_values({'Vehicle.Speed': Datapoint(42)})
    print("After:", client.get_current_values(('Vehicle.Speed',)))
