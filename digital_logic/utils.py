import os
import random
import string


def make_database_url():
    return 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(
        os.getenv('DB_USER', 'postgres'),
        os.getenv('DB_PASSWORD', ''),
        os.getenv('DB_HOST', '127.0.0.1'),
        os.getenv('DB_PORT', '5432'),
        os.getenv('DB_NAME', 'tests'),
    )


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
