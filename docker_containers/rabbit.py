import logging
from functools import partial
from typing import Callable

from .container import DockerContainer
from .utils import wait_is_ready, inside_container

__all__ = ('RabbitContainer',)

logger = logging.getLogger(__name__)


class RabbitContainer(DockerContainer):

    def __init__(self,
                 check_connection_callback: Callable[[str], bool],
                 user: str = 'guest',
                 password: str = 'guest',
                 erlang_cookie: str = 'rabbitmq',
                 image='rabbitmq:3-management-alpine',
                 port_to_expose: int = 5672):

        super().__init__(image=image)
        self.check_connection_callback = check_connection_callback
        self.user = user
        self.password = password
        self.erlang_cookie = erlang_cookie
        self.port_to_expose = port_to_expose

    def _connect(self):
        wait_is_ready(partial(self.check_connection_callback, self.get_connection_url()))

    def start(self):
        self._configure()
        super().start()
        self.reload()
        try:
            self._connect()
        except:
            self.stop()
            raise
        return self

    def _configure(self):
        self.with_exposed_ports(self.port_to_expose)
        self.with_env("RABBITMQ_ERLANG_COOKIE", self.erlang_cookie)
        self.with_env("RABBITMQ_DEFAULT_USER", self.user)
        self.with_env("RABBITMQ_DEFAULT_PASS", self.password)

    def get_connection_url(self) -> str:
        if inside_container():
            return self.get_external_connection_url()

        host = self.get_container_host_ip(self.port_to_expose)
        port = self.get_exposed_port(self.port_to_expose)
        return f'amqp://{self.user}:{self.password}@{host}:{port}/'

    def get_external_connection_url(self) -> str:
        host = self.get_host_ip()
        port = self.port_to_expose
        return f'amqp://{self.user}:{self.password}@{host}:{port}/'
