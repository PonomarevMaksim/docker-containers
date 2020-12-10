import logging
from functools import partial
from typing import Optional, Callable, Any

from .container import DockerContainer
from .utils import wait_is_ready, inside_container

__all__ = ('PostgresContainer',)

logger = logging.getLogger(__name__)


class PostgresContainer(DockerContainer):

    def __init__(self,
                 check_connection_callback: Callable[[str], Any],
                 user: str = 'user',
                 password: str = 'pass',
                 database: Optional[str] = None,
                 image: str = 'postgres:11-alpine',
                 port_to_expose: int = 5432):

        super(PostgresContainer, self).__init__(image=image)
        self.check_connection_callback = check_connection_callback
        self.user = user
        self.password = password
        self.database = database or user
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
        self.with_env("POSTGRES_USER", self.user)
        self.with_env("POSTGRES_PASSWORD", self.password)
        self.with_env("POSTGRES_DB", self.database)

    def get_connection_url(self) -> str:
        if inside_container():
            return self.get_external_connection_url()

        host = self.get_container_host_ip(self.port_to_expose)
        port = self.get_exposed_port(self.port_to_expose)
        return f'postgresql://{self.user}:{self.password}@{host}:{port}/{self.database}?sslmode=disable'

    def get_external_connection_url(self) -> str:
        host = self.get_host_ip()
        port = self.port_to_expose
        return f'postgresql://{self.user}:{self.password}@{host}:{port}/{self.database}?sslmode=disable'

    def get_jdbc_connection_url(self) -> str:
        host = self.get_host_ip()
        port = self.port_to_expose
        return f'jdbc:postgresql://{host}:{port}/{self.database}?sslmode=disable'
