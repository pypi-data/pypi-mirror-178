import asyncio
import logging
import logging.config
from typing import Dict

logging.config.fileConfig('kuksa_client/logging.ini')

from kuksa.val.v1 import types_pb2
from kuksa.val.v1 import val_pb2

import kuksa_client.grpc
from kuksa_client.grpc import Datapoint
from kuksa_client.grpc import EntryRequest
from kuksa_client.grpc import Field
from kuksa_client.grpc import Metadata
from kuksa_client.grpc import View


def on_target_values_updated(updates: Dict[str, Datapoint]):
    for path, dp in updates.items():
        print(f"Target value for {path} is now: {dp.value}")


def on_current_values_updated(updates: Dict[str, Datapoint]):
    for path, dp in updates.items():
        print(f"Current value for {path} is now: {dp.value}")


def on_metadata_updated(updates: Dict[str, Metadata]):
    for path, md in updates.items():
        print(f"Metadata for {path} are now: {md.to_dict()}")


async def start_client():
    forever = asyncio.Event()
    async with kuksa_client.grpc.VSSClient('127.0.0.1', 55555) as client:
        sub_ids = [
            await client.subscribe_current_values([
                'Vehicle.Speed',
                'Vehicle.ADAS.ABS.IsActive',
                'Vehicle.ADAS.CruiseControl.Error',
                'Vehicle.Cabin.Door.Row1.Left.Shade.Position',
            ], on_current_values_updated),
            await client.subscribe_target_values([
                'Vehicle.ADAS.ABS.IsActive',
            ], on_target_values_updated),
            await client.subscribe_metadata([
                'Vehicle.Speed',
                'Vehicle.ADAS.ABS.IsActive',
                'Vehicle.ADAS.CruiseControl.Error',
                'Vehicle.Cabin.Door.Row1.Left.Shade.Position',
            ], on_metadata_updated),
        ]
        try:
            await forever.wait()
        finally:
            for sub_id in sub_ids:
                await client.unsubscribe(sub_id)


def main():
    logging.debug('Starting test...')
    asyncio.run(start_client())

if __name__ == '__main__':
    main()
