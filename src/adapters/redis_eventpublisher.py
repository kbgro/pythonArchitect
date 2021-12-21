import json
import logging
from dataclasses import asdict

import redis

import config
from src.domain import events

logger = logging.getLogger(__name__)

r = redis.Redis(**config.get_redis_host_and_port())


def publish(channel, event: events.Event):
    logging.debug("publishing: channel=%s, event=%s", channel, event)
    r.publish(channel, json.dumps(asdict(event)))
