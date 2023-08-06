# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['imfdatapy']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.5', 'pandas>=1.5.2', 'requests>=2.28.1']

setup_kwargs = {
    'name': 'imfdatapy',
    'version': '0.1.0',
    'description': 'A package for data extraction from the IMF!',
    'long_description': '# imfdatapy\n\nA package for data extraction from the International Monetary Fund (IMF)!\nThis repository contains Python source code and Jupyter notebooks with examples on how to extract data from the IMF.\n\n## Installation\n\n```bash\n$ pip install imfdatapy\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`imfdatapy` was created by Irina Klein and Sou-Cheng T. Choi, Illinois Institute of Technology. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`imfdatapy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Irina Klein, Sou-Cheng T. Choi',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
