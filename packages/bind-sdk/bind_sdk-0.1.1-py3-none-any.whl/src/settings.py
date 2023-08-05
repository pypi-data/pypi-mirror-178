import os

BIND_END_POINT = os.environ.get("BIND_END_POINT", "https://sandbox.bind.com.ar/v1/")
BIND_USER = os.environ.get("BIND_USER", "gustavo.ghioldi@mitrol.net")
BIND_PASSWORD = os.environ.get("BIND_PASSWORD", "fW1sDIqLzGfqAKf")
REDIS_CONNECTION = os.environ.get("REDIS_CONNECTION", True)
