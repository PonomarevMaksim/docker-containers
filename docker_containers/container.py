from typing import Optional

import blindspin
import crayons
from docker.client import DockerClient

from .utils import inside_container

__all__ = ('DockerContainer',)


class DockerContainer:
    def __init__(self, image: str, client: Optional[DockerClient] = None,
                 cmd: Optional[str] = None,
                 network: Optional[str] = None):
        self.env = {}
        self.ports = {}
        self.volumes = {}
        self.links = {}
        self.image = image
        self.network = network
        self._docker = client if client is not None else DockerClient()
        self._command = cmd
        self._container = None
        self._name = None

    def with_env(self, key: str, value: str) -> 'DockerContainer':
        self.env[key] = value
        return self

    def with_link(self, name, link):
        self.links[name] = link
        return self

    def with_bind_ports(self, container: int,
                        host: int = None) -> 'DockerContainer':
        self.ports[container] = host
        return self

    def with_exposed_ports(self, *ports) -> 'DockerContainer':
        for port in list(ports):
            self.ports[port] = self.ports.get(port)
        return self

    def start(self):
        print('')
        print('{} {}'.format(crayons.yellow('Pulling image'),
                             crayons.red(self.image)))
        with blindspin.spinner():
            docker_client = self.get_docker_client()
            self._container = docker_client.containers.run(
                self.image,
                command=self._command,
                detach=True,
                environment=self.env,
                ports=self.ports,
                name=self._name,
                volumes=self.volumes,
                network=self.network,
                links=self.links)
        print('')
        print('Container started: ',
              crayons.yellow(self._container.short_id, bold=True))
        return self

    def stop(self, force=True, delete_volume=True):
        if self._container is not None:
            self._container.remove(force=force, v=delete_volume)

    def wait(self):
        if self._container is None:
            return

        self._container.wait()

    def get_logs(self):
        if self._container is None:
            return ()

        return self._container.logs(stream=True)

    @property
    def name(self):
        if self._container is not None:
            return self._container.name

    @property
    def id(self):
        if self._container is not None:
            return self._container.id

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __del__(self):
        if self._container is not None:
            try:
                self.stop()
            except:
                pass

    def reload(self):
        if self._container is not None:
            self._container.reload()

    def get_container_host_ip(self, port) -> str:
        if inside_container():
            ports = self._container.ports
            return ports[f'{port}/tcp'][0]['HostIp']
        else:
            return '0.0.0.0'

    def get_host_ip(self) -> Optional[str]:
        if self._container is None:
            return None

        return self._container.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']

    def get_exposed_port(self, port) -> str:
        if inside_container():
            return port
        else:
            ports = self._container.ports
            return ports[f'{port}/tcp'][0]['HostPort']

    def with_command(self, command: str) -> 'DockerContainer':
        self._command = command
        return self

    def with_name(self, name: str) -> 'DockerContainer':
        self._name = name
        return self

    def with_volume_mapping(self, host: str, container: str,
                            mode: str = 'ro') -> 'DockerContainer':
        mapping = {'bind': container, 'mode': mode}
        self.volumes[host] = mapping
        return self

    def get_docker_client(self) -> DockerClient:
        return self._docker

    def exec(self, command):
        if self._container is None:
            raise RuntimeError('Container should be started before')

        return self._container.exec_run(command)
