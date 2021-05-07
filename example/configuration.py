from typing import Optional

from starlette.config import Config, environ
from starlette.datastructures import Secret

config = Config("test.env" if environ.get("TESTING", False) else ".env")

DEBUG = config("DEBUG", cast=bool, default=False)
TESTING = config("TESTING", cast=bool, default=False)

DB_DRIVER = config("DB_DRIVER", default="postgres")
DB_HOST = config("DB_HOST", default=None)
DB_PORT = config("DB_PORT", cast=int, default=None)
DB_USER = config("DB_USER", default=None)
DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default=None)
DB_DATABASE = config("DB_DATABASE", default=None)

if DB_DATABASE is not None and TESTING:
    DB_DATABASE = f"test_{DB_DATABASE}"


def make_dsn(
    driver: str,
    user: str,
    password: str,
    host: str,
    port: Optional[int],
    database: Optional[str] = None,
) -> str:
    port_str = ""
    if port is not None:
        port_str = f":{port}"

    database_str = ""
    if database is not None:
        database_str = f"/{database}"
    return f"{driver}://{user}:{password}@{host}{port_str}{database_str}"


DB_DSN = config(
    "DB_DSN",
    default=make_dsn(DB_DRIVER, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE),
)

AMQP_HOST = config("AMQP_HOST", default=None)
AMQP_PORT = config("AMQP_PORT", cast=int, default=None)
AMQP_USER = config("AMQP_USER", default=None)
AMQP_PASSWORD = config("AMQP_PASSWORD", cast=Secret, default=None)
AMQP_QUEUE = config("AMQP_QUEUE", default=None)
AMQP_EXCHANGE = config("AMQP_EXCHANGE", default=None)

if AMQP_QUEUE is not None and TESTING:
    AMQP_QUEUE = f"test_{AMQP_QUEUE}"

if AMQP_EXCHANGE is not None and TESTING:
    AMQP_EXCHANGE = f"test_{AMQP_EXCHANGE}"

AMQP_DSN = config(
    "AMQP_DSN", default=make_dsn("amqp", AMQP_USER, AMQP_PASSWORD, AMQP_HOST, AMQP_PORT)
)

DELAY_ON_EXC = config("DELAY_ON_EXC", default=5.0)
