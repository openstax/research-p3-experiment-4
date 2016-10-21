import os


def make_database_url():
    return 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(
        os.getenv('DB_USER', "postgres"),
        os.getenv('DB_PASSWORD', ''),
        os.getenv('DB_HOST', '127.0.0.1'),
        os.getenv('DB_PORT', '5432'),
        os.getenv('DB_NAME', 'tests'),
    )
