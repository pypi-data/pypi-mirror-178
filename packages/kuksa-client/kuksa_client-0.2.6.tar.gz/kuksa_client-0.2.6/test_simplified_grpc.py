import asyncio
import logging
import logging.config

logging.config.fileConfig('kuksa_client/logging.ini')

from kuksa.val.v1 import types_pb2
from kuksa.val.v1 import val_pb2

import kuksa_client.grpc
from kuksa_client.grpc import Datapoint
from kuksa_client.grpc import DataType
from kuksa_client.grpc import EntryRequest
from kuksa_client.grpc import Field
from kuksa_client.grpc import Metadata
from kuksa_client.grpc import MetadataField
from kuksa_client.grpc import View

async def start_client():
    async with kuksa_client.grpc.VSSClient('127.0.0.1', 55555) as client:
        await client.set_current_values({
            'Vehicle.Speed': Datapoint(42),
            'Vehicle.ADAS.ABS.IsActive': Datapoint(False),
            'Vehicle.ADAS.CruiseControl.Error': Datapoint(False),
            'Vehicle.Cabin.Door.Row1.Left.Shade.Position': Datapoint(12),
        })
        await client.set_target_values({
            'Vehicle.ADAS.ABS.IsActive': Datapoint(True),
        })
        await client.set_metadata({
            'Vehicle.Cabin.Door.Row1.Left.Shade.Position': Metadata(
                data_type=DataType.FLOAT,
            ),
        })
        current_values = await client.get_current_values([
            'Vehicle.Speed',
            'Vehicle.ADAS.ABS.IsActive',
            'Vehicle.ADAS.CruiseControl.Error',
            'Vehicle.Cabin.Door.Row1.Left.Shade.Position',
        ])
        print(f"{current_values=}")
        target_values = await client.get_target_values([
            'Vehicle.ADAS.ABS.IsActive',
        ])
        print(f"{target_values=}")
        metadata = await client.get_metadata([
            'Vehicle.Speed',
            'Vehicle.ADAS.ABS.IsActive',
            'Vehicle.ADAS.CruiseControl.Error',
            'Vehicle.Cabin.Door.Row1.Left.Shade.Position',
        ])
        print(f"{metadata=}")
        speed_unit = metadata['Vehicle.Speed'].unit
        print(f"{speed_unit}")
        speed_data_type = metadata['Vehicle.Speed'].data_type
        print(f"{speed_data_type}")


def main():
    logging.debug('Starting test...')
    asyncio.run(start_client())

if __name__ == '__main__':
    main()
