import asyncio
import logging
import threading
import typing
from types import TracebackType

import aio_pika
from aio_pika.abc import (
    AbstractRobustConnection,
    AbstractRobustChannel,
)
from yarl import URL


def _build_connection_strings(
    host: str,
    port: int,
    vhost: str,
    username: typing.Optional[str],
    password: typing.Optional[str],
    connection_name: typing.Optional[str],
):
    _tmp = URL.build(scheme="amqp", host=host, port=port, path=f"/{vhost}")
    if connection_name:
        _tmp = _tmp.with_query(name=connection_name)
    _url = _url_masked = str(_tmp)
    if username is not None and username is not None:
        _url = str(_tmp.with_user(username).with_password(password))
    return _url, _url_masked


class RabbitMQConnectionProvider:
    def __init__(
        self,
        host: str,
        port: typing.Optional[int] = None,
        vhost: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        connection_name: typing.Optional[str] = None,
    ):
        if port is None:
            port = 5672
        if vhost is None:
            vhost = "/"
        self._url, self._url_masked = _build_connection_strings(
            host=host,
            port=port,
            username=username,
            password=password,
            vhost=vhost,
            connection_name=connection_name,
        )
        self._conn: typing.Optional[AbstractRobustConnection] = None
        self._get_loop = lambda: asyncio.get_running_loop()
        self._lock = threading.Lock()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.debug("New instance")

    async def __aenter__(
        self,
    ) -> "RabbitMQConnectionProvider":
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[TracebackType],
    ) -> None:
        await self.close()

    async def close(self) -> None:
        if self._conn and not self._conn.is_closed:
            with self._lock:
                if self._conn and not self._conn.is_closed:
                    self.logger.info(f"Closing connection to RabbitMQ on {self._conn}")
                    await self._conn.close()

    async def open_channel(self, **kwargs) -> AbstractRobustChannel:
        con = await self.reuse_connection()
        return con.channel(**kwargs)

    async def reuse_connection(self) -> AbstractRobustConnection:
        if not self._conn or self._conn.is_closed:
            with self._lock:
                if not self._conn or self._conn.is_closed:
                    self._conn = await self.open_connection()
        return self._conn

    async def open_connection(self) -> AbstractRobustConnection:
        try:
            self.logger.debug(f"Connecting to RabbitMQ on {self._url_masked}")
            return await aio_pika.connect_robust(self._url, loop=self._get_loop())
        finally:
            self.logger.info(f"Connected to RabbitMQ on {self._url_masked}")
