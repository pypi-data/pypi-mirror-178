# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['neurorosettes']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0', 'pydantic>=1.9.0,<2.0.0', 'vedo>=2022.0.1,<2023.0.0']

entry_points = \
{'console_scripts': ['cell_cell = examples.mechanics.test_sphere_sphere:main',
                     'neurite_cell = '
                     'examples.mechanics.test_sphere_neurite:main',
                     'neurite_neurite = '
                     'examples.mechanics.test_neurite_neurite:main',
                     'rosette_formation = examples.rosette_formation:main',
                     'sweep_mechanics = examples.sweep_mechanics:main']}

setup_kwargs = {
    'name': 'neurorosettes',
    'version': '0.1.1',
    'description': 'A computational modelling framework designed to simulate the formation of rosette patterns in tissues of the nervous system.',
    'long_description': '# neurorosettes\n> An agent-based framework to model the formation of rosette patterns in tissues of the nervous system\n\n`neurorosettes` is a Python package that implements agent-based modelling to study the formation of rosette patterns in tissues\nduring neuronal development. It is built on top of the `vedo` package (version 2022.1.0), which provides an interface\nto plot 3D objects using VTK, to prioritize the visualization of the simulations in real time, without requiring additional processing.\n\n## Installation\n\nThe package can be downloaded through pip using `pip install neurorosettes`.\n\n## Usage\n\n`neurorosettes` offers multiple modules to simulate and test new biological hypothesis, such as:\n- Cell cycle and death;\n- Creation and extension of neuronal processes;\n- Physical interactions between cell bodies and neuronal processes;',
    'author': 'Inês G Gonçalves',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
