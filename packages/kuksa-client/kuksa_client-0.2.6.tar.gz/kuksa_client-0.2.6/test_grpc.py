import asyncio
import logging
import logging.config

logging.config.fileConfig('kuksa_client/logging.ini')

from kuksa.val.v1 import types_pb2
from kuksa.val.v1 import val_pb2

import kuksa_client.grpc
from kuksa_client.grpc import Datapoint, EntryRequest, Field, View, EntryUpdate, DataEntry, VSSClientError
from kuksa_client.grpc import Metadata
from kuksa_client.grpc import DataType

def callback(updates):
    print(list(update for update in updates))


async def start_client():
    async with kuksa_client.grpc.VSSClient('127.0.0.1', 55555) as client:
        """
        entries = await client.get(entries=[
            EntryRequest('Vehicle.Speed', View.CURRENT_VALUE, (Field.VALUE,)),
            EntryRequest('Vehicle.ADAS.ABS.IsActive', View.TARGET_VALUE, (Field.ACTUATOR_TARGET,)),
            EntryRequest('Vehicle.ADAS.CruiseControl.Error', View.METADATA, (Field.METADATA,)),
            EntryRequest('Vehicle.ADAS.CruiseControl.Error', View.METADATA, (Field.METADATA_DATA_TYPE,)),
            EntryRequest('Vehicle.ADAS.CruiseControl.Error', View.METADATA, (Field.METADATA_DESCRIPTION,)),
            EntryRequest('Vehicle.ADAS.CruiseControl.Error', View.METADATA, (Field.METADATA_ENTRY_TYPE,)),
            EntryRequest('Vehicle.ADAS.CruiseControl.Error', View.METADATA, (Field.METADATA_COMMENT,)),
            EntryRequest('Vehicle.ADAS.CruiseControl.Error', View.METADATA, (Field.METADATA_DEPRECATION,)),
            EntryRequest('Vehicle.Cabin.Door.Row1.Left.Shade.Position', View.METADATA, (Field.METADATA_UNIT,)),
            EntryRequest('Vehicle.Cabin.Door.Row1.Left.Shade.Position', View.METADATA, (Field.METADATA_VALUE_RESTRICTION,)),
        ])
        """
        #await client.get(entries=[])
        #await client.set(updates=[])
        await client.subscribe(entries=[], callback=None)
        """
        sub_uid = await client.subscribe(entries=(entry for entry in (  # generator is intentional (Iterable)
            EntryRequest('Does.Not.Exist', View.CURRENT_VALUE, (Field.VALUE,)),
        )), callback=callback)
        """


def main():
    logging.debug('Starting test...')
    asyncio.run(start_client())

if __name__ == '__main__':
    main()
