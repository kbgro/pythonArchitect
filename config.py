import os

from dotenv import load_dotenv

load_dotenv()


def get_postgres_uri():
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    user = os.environ.get("DB_USER")
    db_name = os.environ.get("DB_NAME")
    password = os.environ.get("DB_PASSWORD")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.environ.get("API_HOST")
    port = os.environ.get("API_PORT")
    return f"http://{host}:{port}"


def get_redis_host_and_port():
    host = os.environ.get("REDIS_HOST")
    port = os.environ.get("REDIS_PORT")
    return dict(host=host, port=port)
