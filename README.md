# docker_containers

## Usage:
```python
import time

from x5_aio_pika_ext import RMQClient

from docker_containers import RabbitContainer


async def check_connect(url):
    rabbit_client = RMQClient(url)
    await rabbit_client.is_alive()
    await rabbit_client.close()


container = RabbitContainer(check_connect)

container.start()
time.sleep(180)
container.stop()

```