from typing import Optional

from docker import DockerClient
from docker.models.images import Image

__all__ = ('BuildDockerImage',)


class BuildDockerImage:

    def __init__(self, path: str,
                 client: Optional[DockerClient] = None):
        self._docker_file_path = path
        self._client = client or DockerClient()
        self._image: Optional[Image] = None

    def __enter__(self):
        self.build()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remove()

    def build(self):
        self._image, _ = self._client.images.build(self._docker_file_path)

    def get_image_id(self):
        return self._image.id

    def remove(self):
        if self._image is not None:
            self._client.images.remove(self._image)

    def __del__(self):
        self.remove()
