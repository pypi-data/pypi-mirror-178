# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wp-client-aio']

package_data = \
{'': ['*']}

install_requires = \
['aiodns==3.0.0',
 'aiohttp==3.8.1',
 'aiosignal==1.2.0',
 'astroid>=2.12.13,<3.0.0',
 'async-timeout==4.0.1',
 'attrs==21.2.0',
 'brotli==1.0.9',
 'cchardet==2.1.7',
 'cffi==1.15.0',
 'charset-normalizer==2.0.9',
 'frozenlist==1.2.0',
 'idna==3.3',
 'lazy-object-proxy>=1.8.0,<2.0.0',
 'multidict==5.2.0',
 'platformdirs==2.4.0',
 'pycares==4.1.2',
 'pycparser>=2.21,<3.0',
 'wrapt>=1.14.1,<2.0.0',
 'yarl==1.7.2']

setup_kwargs = {
    'name': 'wp-client-aio',
    'version': '1.0.4',
    'description': '',
    'long_description': '# wp-client-aio\n\nWordPress REST API Python Client based on aiohttp python library\n\n## Installation\n\n```bash\npip install wp-client-aio\n```\n\n## Usage\n\nCreate new client\n\n```python\nwp_client = WordpressRestApiClient(\n    os.environ.get("URL"),\n    os.environ.get("WP_USER"),\n    os.environ.get("WP_PASS")\n)\n```\n\n\nCall API\n\n```python\n    await asyncio.gather(\n        wp_client.get(client, endpoint = 2),\n        wp_client.delete(client, endpoint = 3),\n        wp_client.get(client),\n        wp_client.post(client,\n            payload =\n                {\n                    "title": "Lorem Ipsum",\n                    "content": "Lorem ipsum sit amet",\n                    "status": "publish"\n                }\n            ),\n\n        wp_client.patch(client, endpoint=4, payload = {\n            "title": "Съешь ещё этих мягких французских булок",\n        }),\n        wp_client.put(client, endpoint=4,\n            payload =\n                {\n                    "title": "съешь ещё этих мягких французских булок",\n                    "content": "Да выпей чаю",\n                    "status": "publish"\n                }\n            ),\n    )\n```\n',
    'author': 'Maxim Yurevich',
    'author_email': 'maxim.yurewitch@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
