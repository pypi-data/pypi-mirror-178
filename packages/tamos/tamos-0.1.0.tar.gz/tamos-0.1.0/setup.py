# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tamos',
 'tamos.data_IO',
 'tamos.element',
 'tamos.elementIO',
 'tamos.network',
 'tamos.production',
 'tamos.solve_tools',
 'tamos.storage']

package_data = \
{'': ['*']}

install_requires = \
['docplex>=2.24.0',
 'matplotlib>3.0.0',
 'networkx>=2.8',
 'numpy>=1.0.0',
 'pandas>=1',
 'scipy',
 'sympy']

setup_kwargs = {
    'name': 'tamos',
    'version': '0.1.0',
    'description': 'Thermal Architectures Modelling and Optimization Software',
    'long_description': '# tamos\n\n## What does "tamos" stand for?\n"tamos" stands for Thermal Architectures Modelling and Optimization Software.\n\n## What is it?\n`tamos` is a non-GUI tool that aims at facilitating the study of thermal architectures.\nA thermal architecture is a set of energy production, storage and distribution components that operate together in order to meet some energy demands.\n\n## How does it work? \n`tamos` performs the optimal sizing and operation of various energy components gathered in energy hubs.\nIt relies on the description of these components using the Mixed-Integer Linear Programming formalism (MILP), i.e. mathematical programming.\n\n## What are the main software components?\n`tamos` heavily relies on the `docplex` api, that eases the formulation of MILP problems.\nOnce declared, the problems are solved using the Cplex solver. It can also be exported to `.LP` and `.MPS` formats and be solved using non-proprietary solvers. \n\n##  Installation notes\nThe packaged version of `tamos`is available on PyPi. Please run:\n`pip install tamos`\n\n\n## Where is project hosted?\nSources are managed on GitHub: https://github.com/BNerot/tamos/tree/main/src/tamos \nThe file `Batch analysis.ipynb` is only on GitHub. It provides the user with an easy way to analyse large volumes of results.\n\n## Is it difficult to use?\nPlease follow one of the two examples in `examples` as a quick start guide. \nYou can also find a web version of the documentation in `docs/build/html`. Once this directory is downloaded, please open \'index.html\'. \n\n## Copyright\nThe code is distributed under an Apache-2.0 license. \nMost of the development work was done in the context of a PhD thesis. \nThis thesis was funded by two French institutions:\n- Commissariat à l\'Energie Atomique: https://www.cea.fr/english\n- Agence de la transition écologique: https://www.ademe.fr/en/frontpage/\n',
    'author': 'BNerot',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
