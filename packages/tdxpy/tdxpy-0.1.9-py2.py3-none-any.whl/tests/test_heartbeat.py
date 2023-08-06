# test test_heartbeat.py
import time

from tdxpy.hq import TdxHq_API
from tdxpy.logger import logger


def test_heartbeat(bestip, caplog):
    api = TdxHq_API(heartbeat=True, auto_retry=True)
    api.heartbeat_interval = 1

    assert api.connect(ip=bestip[0], port=int(bestip[1]))
    assert api.heartbeat_thread.is_alive()

    logger.debug('Test: sleep 3s')
    time.sleep(3)

    logger.debug('Test: 关闭心跳')
    api.disconnect()

    logger.debug('Test: sleep 3s')
    time.sleep(.1)
    assert not api.heartbeat_thread.is_alive()


def test_multithread(bestip, caplog):
    api = TdxHq_API(multithread=True, auto_retry=True)
    api.connect(ip=bestip[0], port=bestip[1])
    assert api.lock

    api.disconnect()

