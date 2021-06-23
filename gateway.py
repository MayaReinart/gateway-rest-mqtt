#!/usr/bin/env python3
import sys
import getopt
import asyncio
from aiohttp import web
import asyncio_mqtt
import logging
import typing

routes = web.RouteTableDef()


async def mqtt_connect(mqtt_address: str) -> asyncio_mqtt.Client:
    mqtt_client = asyncio_mqtt.Client(mqtt_address)
    await mqtt_client.subscribe('system/+/out/#')
    return mqtt_client


async def mqtt_receive_report(mqtt_client: asyncio_mqtt.Client):
    ...


@routes.get('/{device_id}/app/command')
async def process_request(request: str) -> web.Response:
    logging.info(f'Received request: {request}')
    ...
    return web.Response()


async def init():
    mqtt_address = 'localhost:1883/'
    log_file_name = None

    usage = 'Usage: gateway.py --mqtt-address <address> --log <log file>'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['mqtt-address=', 'log='])
    except getopt.GetoptError:
        print(usage)
        return 1
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            return 1
        elif opt == '--mqtt-address':
            mqtt_address = arg
        elif opt == '--log':
            log_file_name = arg

    if log_file_name is not None:
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                            level=logging.INFO,
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=log_file_name)

    mqtt_client = await mqtt_connect(mqtt_address)
    app = web.Application()
    app.add_routes(routes)
    loop.create_task(mqtt_receive_report(mqtt_client))
    logging.info('Gateway has started')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    loop.run_forever()
