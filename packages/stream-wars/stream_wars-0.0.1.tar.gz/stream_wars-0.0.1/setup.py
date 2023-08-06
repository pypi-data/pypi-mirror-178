# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stream_wars']

package_data = \
{'': ['*'], 'stream_wars': ['frontend/build/*']}

install_requires = \
['streamlit>=1.11.1,<2.0.0']

setup_kwargs = {
    'name': 'stream-wars',
    'version': '0.0.1',
    'description': 'Streamlit component to generate the Star Wars crawl text.',
    'long_description': 'None',
    'author': 'Murilo Cunha',
    'author_email': 'murilo@dataroots.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
