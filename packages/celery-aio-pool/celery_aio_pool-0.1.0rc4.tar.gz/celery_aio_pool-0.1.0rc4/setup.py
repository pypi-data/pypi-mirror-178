# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['celery_aio_pool']

package_data = \
{'': ['*']}

install_requires = \
['celery>=5,<6']

setup_kwargs = {
    'name': 'celery-aio-pool',
    'version': '0.1.0rc4',
    'description': 'Celery worker pool with support for asyncio coroutines as tasks',
    'long_description': '# Celery AsyncIO Pool\n\n![python](https://img.shields.io/pypi/pyversions/celery-aio-pool.svg)\n![version](https://img.shields.io/pypi/v/celery-aio-pool.svg)\n![downloads](https://img.shields.io/pypi/dm/celery-aio-pool.svg)\n![format](https://img.shields.io/pypi/format/celery-aio-pool.svg)\n\n<p align="center" width="100%">\n    <img width="55%" src="https://raw.githubusercontent.com/the-wondersmith/celery-aio-pool/main/icon.svg">\n</p>\n\n> Free software: GNU Affero General Public License v3+\n\n## Getting Started\n\n### Installation\n\n#### Using Poetry _(preferred)_\n\n```\npoetry add celery-aio-pool\n```\n\n#### Using `pip` & [PyPI.org](https://pypi.org/project/celery-aio-pool/)\n\n```\npip install celery-aio-pool\n```\n\n#### Using `pip` & [GitHub](https://github.com/the-wondersmith/celery-aio-pool.git)\n\n```\npip install git+https://github.com/the-wondersmith/celery-aio-pool.git\n```\n\n### Using `pip` & A Local Copy Of The Repo\n\n```\ngit clone https://github.com/the-wondersmith/celery-aio-pool.git\ncd celery-aio-pool\npip install -e "$(pwd)"\n```\n\n\n### Configure Celery\n\n#### Using `celery-aio-pool`\'s Provided Patcher _(non-preferred)_\n\n- Import `celery_aio_pool` in the same module where your Celery "app" is defined\n- Ensure that the `patch_celery_tracer` utility is called **_before_** any other\n  Celery code is called\n\n```python\n"""My super awesome Celery app."""\n\n# ...\nfrom celery import Celery\n\n# add the following import\nimport celery_aio_pool as aio_pool\n\n# ensure the patcher is called *before*\n# your Celery app is defined\n\nassert aio_pool.patch_celery_tracer() is True\n\napp = Celery(\n    "my-super-awesome-celery-app",\n    broker="amqp://guest@localhost//",\n    # add the following keyword argument\n    worker_pool=aio_pool.pool.AsyncIOPool,\n)\n```\n\n#### Using (Upcoming) _Out-Of-Tree_ Worker Pool _(preferred)_\n\nAt the time of writing, [Celery](https://github.com/celery/celery) does not have\nbuilt-in support for out-of-tree pools like `celery-aio-pool`, but support should\nbe included starting with the first non-beta release of Celery 5.3. (note: [PR #7880](https://github.com/celery/celery/pull/7880) was merged on `2022-11-15`).\n\nThe official release of Celery 5.3 enables the configuration of custom worker pool classes thusly:\n\n- Set the environment variable `CELERY_CUSTOM_WORKER_POOL` to the name of\n  your desired worker pool implementation implementation.\n  - **NOTE:** _The value of the environment variable must be formatted in\n              the standard Python/Celery format of_ `package:class`\n  - ```bash\n    % export CELERY_CUSTOM_WORKER_POOL=\'celery_aio_pool.pool:AsyncIOPool\'\n    ```\n\n- Tell Celery to use your desired pool by specifying `--pool=custom` when running your worker instance(s)\n  - ```bash\n    % celery worker --pool=custom --loglevel=INFO --logfile="$(pwd)/worker.log"\n    ```\n\nTo verify the pool implementation, examine the output of the `celery inspect stats`\ncommand:\n\n```bash\n% celery --app=your_celery_project inspect stats\n->  celery@freenas: OK\n    {\n        ...\n        "pool": {\n           ...\n            "implementation": "celery_aio_pool.pool:AsyncIOPool",\n    ...\n```\n\n\n## Developing / Testing / Contributing\n\n> **NOTE:** _Our preferred packaging and dependency manager is [Poetry](https://python-poetry.org/)._\n>           _Installation instructions can be found [here](https://python-poetry.org/docs/#installing-with-the-official-installer)._\n\n### Developing\n\nClone the repo and install the dependencies\n```bash\n$ git clone https://github.com/the-wondersmith/celery-aio-pool.git \\\n  && cd celery-aio-pool \\\n  && poetry install --sync\n```\n\nOptionally, if you do not have or prefer _not_ to use Poetry, `celery-aio-pool` is\nfully PEP-517 compliant and can be installed directly by any PEP-517-compliant package\nmanager.\n\n```bash\n$ cd celery-aio-pool \\\n  && pip install -e "$(pwd)"\n```\n\n> **TODO:** _Coming Soon™_\n\n### Testing\n\nTo run the test suite:\n\n```bash\n$ poetry run pytest tests/\n```\n\n### Contributing\n\n> **TODO:** _Coming Soon™_\n',
    'author': 'Mark S.',
    'author_email': 'the@wondersmithd.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/the-wondersmith/celery-aio-pool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
