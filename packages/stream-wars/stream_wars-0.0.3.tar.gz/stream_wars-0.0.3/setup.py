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
    'version': '0.0.3',
    'description': 'Streamlit component to generate the Star Wars crawl text.',
    'long_description': '<p align="center">\n  <a href="https://github.com/murilo-cunha/stream-wars"><img width="50%" alt="logo" src="https://raw.githubusercontent.com/murilo-cunha/stream-wars/main/images/stream-wars-logo.png"></a>\n</p>\n<p align="center">\n  <a href="https://pypi.org/project/stream-wars/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/stream-wars" /></a>\n  <a href="https://pypi.org/project/stream-wars/"><img alt="PiPy" src="https://img.shields.io/pypi/v/stream-wars" /></a>\n  <a href="https://pepy.tech/project/stream-wars"><img alt="Downloads" src="https://pepy.tech/badge/stream-wars" /></a>\n  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>\n  <a href="http://mypy-lang.org/"><img alt="Mypy checked" src="https://img.shields.io/badge/mypy-checked-1f5082.svg" /></a>\n</p>\n\n> A Star Wars crawl component for Streamlit apps!\n\nA wrapper around [`star-wars-crawl-greensock-with-hooks`](https://github.com/mandiwise/star-wars-crawl-greensock-with-hooks)\nby [@mandiwise](https://github.com/mandiwise), using the\n[`streamlit-component-template-react-hooks`](https://github.com/whitphx/streamlit-component-template-react-hooks)\nby [@whitphx](https://github.com/whitphx) (credits to them! 👏👏).\n\n## Details\n\nThis is a small project putting together a "Star Wars" crawl component written in React and a React hooks-based template for Streamlit apps.\n\nWhy? The official documentation lists the class based components for React. React has released the hook-based API, which is arguably simpler and generally preferred over the class based components. Personally, I also prefer hook-based components over class-based ones. The project also uses `poetry` over the official documentation\'s `setup.py` and `MANIFEST.in` files - another personal decision.\n\n## Features\n\n- [x] Custom button\n- [x] Custom intro\n- [x] Custom episode text\n- [x] Custom episode title\n- [x] Custom crawl content\n- [ ] Available on `wide` layout\n',
    'author': 'Murilo Cunha',
    'author_email': 'murilo@dataroots.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://murilo-cunha-stream-wars-stream-warsdocs-slmccu.streamlit.app/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
