# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['semantic_tree']

package_data = \
{'': ['*']}

install_requires = \
['gensim>=4.2.0,<5.0.0', 'matplotlib>=3.6.2,<4.0.0', 'networkx>=2.8.8,<3.0.0']

entry_points = \
{'console_scripts': ['semanticTree = semantic_tree.semtree:run',
                     'semanticTreeDemo = semantic_tree.semtree:demo']}

setup_kwargs = {
    'name': 'semantic-tree',
    'version': '1.1.1',
    'description': "Creates a visualization of the semantic neighborhood of a word in a Gensim's Word2Vec vector space model using the Gource visualizer",
    'long_description': '\n# Semantic Tree\n\n\n\nThis package provide a semanticTree command, which generates a visualization of the semantic neighborhood of a work in a Gensim Word2vec vector space.\n\n\n## Installation\n\n\nThis package requires that [Gource](https://gource.io/) is installed locally. On Ubuntu, it can be apt installed.\n\n```bash\n$ apt install gource\n```\n\nSemanticTree itself can be installed from PyPI with `pip`.\n\n ```\n pip install -U semantic_tree\n ```\n\n![Screenshot](screen.png)\n## Note\n\n\nThis project has been set up using PyScaffold 3.2.3. For details and usage\ninformation on PyScaffold see https://pyscaffold.org/.\n',
    'author': 'Flávio Codeço Coelho',
    'author_email': 'fccoelho@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fccoelho/SemanticTree',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
