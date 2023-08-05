# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_data_structures']

package_data = \
{'': ['*']}

entry_points = \
{'manim.plugins': ['manim_data_structures = manim_data_structures']}

setup_kwargs = {
    'name': 'manim-data-structures',
    'version': '0.1.0',
    'description': 'A Manim implementation for data structures',
    'long_description': '',
    'author': 'Hammad Nasir',
    'author_email': 'hammadn99@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/drageelr/manim-data-structures',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
