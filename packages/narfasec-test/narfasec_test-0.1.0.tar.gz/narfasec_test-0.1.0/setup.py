# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['example_package_narfasec']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['sherlog = entry:main']}

setup_kwargs = {
    'name': 'narfasec-test',
    'version': '0.1.0',
    'description': 'Just a test',
    'long_description': '# Example Package\n\nThis is a simple example package. You can use\n[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)\nto write your content.',
    'author': 'narfasec',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
