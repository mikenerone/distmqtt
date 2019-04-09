import logging
import anyio

from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.mqtt.constants import QOS_1, QOS_2


#
# This sample shows how to publish messages to broker using different QOS
# Debug outputs shows the message flows
#

logger = logging.getLogger(__name__)

config = {
    'will': {
        'topic': '/will/client',
        'message': b'Dead or alive',
        'qos': 0x01,
        'retain': True
    }
}


async def test_coro():
    C = MQTTClient()
    await C.connect('mqtt://test.mosquitto.org/')
    try:
        async with anyio.open_task_group() as tg:
            await tg.spawn(C.publish,'a/b', b'TEST MESSAGE WITH QOS_0')
            await tg.spawn(C.publish,'a/b', b'TEST MESSAGE WITH QOS_1', qos=QOS_1)
            await tg.spawn(C.publish,'a/b', b'TEST MESSAGE WITH QOS_2', qos=QOS_2)
        logger.info("messages published")
    finally:
        await C.disconnect()


async def test_coro2():
    try:
        C = MQTTClient()
        async with C.broker('mqtt://test.mosquitto.org:1883/'):
            await C.publish('a/b', b'TEST MESSAGE WITH QOS_0', qos=0x00)
            await C.publish('a/b', b'TEST MESSAGE WITH QOS_1', qos=0x01)
            await C.publish('a/b', b'TEST MESSAGE WITH QOS_2', qos=0x02)
            logger.info("messages published")
    except ConnectException as ce:
        logger.error("Connection failed: %s" % ce)


if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    formatter = "%(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)
    anyio.run(test_coro)
    anyio.run(test_coro2)
