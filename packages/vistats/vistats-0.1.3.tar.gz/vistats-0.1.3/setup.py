# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vistats']

package_data = \
{'': ['*']}

install_requires = \
['ipykernel>=6.17.1,<7.0.0',
 'matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.23.5,<2.0.0',
 'pandas>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'vistats',
    'version': '0.1.3',
    'description': 'package of visualization for statistical tests.',
    'long_description': "# vistats\nVisualization for statistical tests.\n\n## Background\nWe would like to \nwrite a line and asterisks between bars when we get a statistically significant difference by a statistical test. However, there is no appropriate package for visualizing them with 'matplotlib'. This package provides them.\n\n## Installation\n\n```\npip install vistats\n```\n\n## Usage\nPlease see [here](https://github.com/takato86/vistats/blob/main/examples/barplot_example.ipynb)\n",
    'author': 'takato86',
    'author_email': 'okudo@nii.ac.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/takato86/vistats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
