# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asvc',
 'asvc.backends',
 'asvc.backends.kafka',
 'asvc.backends.nats',
 'asvc.backends.rabbitmq',
 'asvc.backends.redis',
 'asvc.encoders',
 'asvc.middlewares',
 'asvc.utils']

package_data = \
{'': ['*']}

install_requires = \
['async-timeout>=4.0.2,<5.0.0', 'pydantic>=1.9.1,<2.0.0']

extras_require = \
{'all': ['aiorun>=2022.4.1,<2023.0.0',
         'click>=8.1.3,<9.0.0',
         'orjson>=3.7.1,<4.0.0',
         'ormsgpack>=1.2.3,<2.0.0',
         'prometheus-client>=0.14.1,<0.15.0',
         'opentelemetry-api>=1.13.0,<2.0.0',
         'opentelemetry-sdk>=1.13.0,<2.0.0',
         'nats-py>=2.1.3,<3.0.0',
         'aioredis>=2.0.1,<3.0.0',
         'aiokafka>=0.7.2,<0.8.0',
         'aio-pika>=8.0.3,<9.0.0',
         'gcloud-aio-pubsub>=5.0.0,<6.0.0'],
 'cli': ['aiorun>=2022.4.1,<2023.0.0', 'click>=8.1.3,<9.0.0'],
 'kafka': ['aiokafka>=0.7.2,<0.8.0'],
 'msgpack': ['ormsgpack>=1.2.3,<2.0.0'],
 'nats': ['nats-py>=2.1.3,<3.0.0'],
 'opentelemetry': ['opentelemetry-api>=1.13.0,<2.0.0',
                   'opentelemetry-sdk>=1.13.0,<2.0.0'],
 'orjson': ['orjson>=3.7.1,<4.0.0'],
 'prometheus': ['prometheus-client>=0.14.1,<0.15.0'],
 'pubsub': ['gcloud-aio-pubsub>=5.0.0,<6.0.0'],
 'rabbitmq': ['aio-pika>=8.0.3,<9.0.0'],
 'redis': ['aioredis>=2.0.1,<3.0.0']}

entry_points = \
{'console_scripts': ['asvc = asvc.cli:cli']}

setup_kwargs = {
    'name': 'asvc',
    'version': '0.1.0',
    'description': 'Event driven microservice framework for python',
    'long_description': '# aio-services\n![Checks](https://img.shields.io/github/checks-status/RaRhAeu/aio-services/main)\n![CI](https://github.com/RaRhAeu/aio-services/workflows/CI/badge.svg)\n![Build](https://github.com/RaRhAeu/aio-services/workflows/Publish/badge.svg)\n![Code Coverage](https://codecov.io/gh/RaRhAeu/aio-services/branch/main/graph/badge.svg)\n![License](https://img.shields.io/github/license/RaRhAeu/aio-services)\n![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)\n![Python](https://img.shields.io/pypi/pyversions/asvc)\n![Format](https://img.shields.io/pypi/format/asvc)\n![PyPi](https://img.shields.io/pypi/v/asvc)\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n\n*Event driven microservice framework for python*\n\n---\n\n## About\n\nThe package utilizes `pydantic` as the only required dependency.\nFor message format Cloud Events format is used.\nService can be run as standalone processes, or included into starlette (e.g. FastAPI) applications.\n\n## Multiple broker support (in progress)\n\n- Stub (in memory using `asyncio.Queue` for PoC, local development and testing)\n- NATS (with JetStream)\n- Redis Pub/Sub\n- Kafka\n- Rabbitmq\n- Google Cloud PubSub\n\n## Optional Dependencies\n  - `cli` - `click` and `aiorun`\n  - `uvloop`\n  - broker of choice: `nats`, `kafka`, `rabbitmq`, `redis`, `pubsub`\n  - custom serializer `msgpack`, `orjson`\n  - `prometheus` - Metric exposure via `PrometheusMiddleware`\n  - `opentelemetry`\n\n\n## Motivation\n\nPython has many "worker-queue" libraries and frameworks, such as:\n    - Celery\n    - Dramatiq\n    - Huey\n    - arq\n\nHowever, those libraries don\'t provide a pub/sub pattern, useful for creating\nevent driven and loosely coupled systems. Furthermore, the majority of those libraries\ndo not support `asyncio`. This is why this project was born.\n\n## Basic usage\n\n\n```python\nimport asyncio\nfrom asvc import Service, CloudEvent\nfrom asvc import Middleware\nfrom asvc.backends.nats.broker import JetStreamBroker\n\n\nbroker = JetStreamBroker(url="nats://localhost:4222")\n\nservice = Service(name="example-service", broker=broker)\n\n\nclass SendMessageMiddleware(Middleware):\n    async def after_service_start(self, broker, service: Service):\n        print(f"After service start, running with {broker}")\n        await asyncio.sleep(10)\n        for i in range(100):\n            await service.publish("test.topic", data={"counter": i})\n        print("Published event(s)")\n\n\nbroker.add_middleware(SendMessageMiddleware())\n\n\n@service.subscribe("test.topic")\nasync def example_run(message: CloudEvent):\n    print(f"Received Message {message.id} with data: {message.data}")\n\n```\n\n\n## Scaling\n\nEach message is load-balanced (depending on broker) between all service instances with the same `name`.\nTo scale number of processes you can use containers (docker/k8s), [supervisor](http://supervisord.org/),\nor web server like gunicorn.\n\n\n## TODOS:\n\n- Automatic [Async Api](https://www.asyncapi.com/) docs generation from service definition.\n- More tests\n  - Integration tests with docker-compose and all backends\n- [OpenTelemetry](https://opentelemetry.io/) Middleware\n- More backends (zeromq, pulsar, solace?)\n- Pluggable logger interface (for third party integrations)\n- Docs + tutorials',
    'author': 'Radzim Kowalow',
    'author_email': 'radzim_ko@wp.pl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
