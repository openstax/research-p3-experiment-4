import os

import redis
from rq import Worker, Queue, Connection

from digital_logic import create_app

app = create_app()
ctx = app.test_request_context()
ctx.push()

listen = ['default']

redis_url = os.getenv('REDISTO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
