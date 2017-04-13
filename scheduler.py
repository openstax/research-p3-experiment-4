import logging
import os

import redis
from rq.utils import ColorizingStreamHandler
from rq_scheduler.scheduler import Scheduler as RQScheduler

redis_url = os.getenv('REDISTO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)


def setup_loghandlers(level='INFO'):
    logger = logging.getLogger('scheduler')
    if not logger.handlers:
        logger.setLevel(level)
        formatter = logging.Formatter(fmt='%(asctime)s %(message)s',
                                      datefmt='%H:%M:%S')
        handler = ColorizingStreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

setup_loghandlers()
logger = logging.getLogger('scheduler')


if __name__ == '__main__':
    scheduler = RQScheduler(connection=conn)
    logger.info('Starting scheduler')
    scheduler.run()
