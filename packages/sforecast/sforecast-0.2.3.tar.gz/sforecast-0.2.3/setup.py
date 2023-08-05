# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sforecast']

package_data = \
{'': ['*']}

install_requires = \
['beautifulplots>=0.2.6',
 'pandas>=1.4.0',
 'pmdarima>=1.8.0',
 'sklearn>=0.0',
 'statsmodels>=0.13.2',
 'tensorflow>=2.7.0']

setup_kwargs = {
    'name': 'sforecast',
    'version': '0.2.3',
    'description': 'A framework for running forecasting models within a sliding/expanding window, including support of classical forecasting models, SK Learn supervised learning ML models, and TensorFlow deep learning models.',
    'long_description': '# sforecast\n\nA package to support supervised learning forecast methods (ML and DL) within a sliding forecast framework (sliding or expanding window)\n\n## Installation\n\n```bash\n$ pip install sforecast\n```\n\n## License\n\n`sforecast` was created by Alberto Gutierrez. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`sforecast` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Alberto Gutierrez',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
