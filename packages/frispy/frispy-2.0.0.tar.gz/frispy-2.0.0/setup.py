# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frispy']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0', 'numpy>=1.23.5,<2.0.0', 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'frispy',
    'version': '2.0.0',
    'description': 'Frisbee simulation.',
    'long_description': '.. |TRAVIS| image:: https://github.com/tmcclintock/FrisPy/workflows/Build%20Status/badge.svg?branch=master\n\t    :target: https://github.com/tmcclintock/FrisPy/actions\n.. |COVERALLS| image:: https://coveralls.io/repos/github/tmcclintock/FrisPy/badge.svg?branch=master\n\t       :target: https://coveralls.io/github/tmcclintock/FrisPy?branch=master\n.. |LICENSE| image:: https://img.shields.io/badge/License-MIT-yellow.svg\n\t     :target: https://opensource.org/licenses/MIT\n\n|TRAVIS| |COVERALLS| |LICENSE|\n\nFrisPy\n======\n\nDocumentation for ``FrisPy`` package can be `found here on RTD\n<https://frispy.readthedocs.io/en/latest/>`_.\n\nThis repository contains a physical model for a flying disc. Using this code,\none can simulate trajectories of discs with varying initial conditions, while\nalso changing the underlying physical model. This is useful for analyzing\nthe mechanics of a disc in terms of its design, as well as creating simulated\nthrows for things like disc launchers or other helpful tools.\n\nThis is a pure Python rebuild of the old FrisPy code, which included a version\nof the integrator written in C for speed. Find the fast C simulation in the\n`Frisbee_Simulator <https://github.com/tmcclintock/Frisbee_Simulator>`_\nrepository.\n\nThe earliest implementation of this model that I could find was by Sara Ann Hummel\nfor their 2003 Masters thesis for UC Davis.  You can find the document in full\n`on this page <https://morleyfielddgc.files.wordpress.com/2009/04/hummelthesis.pdf>`_.\n\nInstallation\n------------\n\nThe easiest way to install this package is with ``pip``. The PyPI package can\nbe viewed `here <https://pypi.org/project/frispy/>`_.\n\n.. code-block:: bash\n\n   pip install frispy\n\n\nFor developers\n--------------\n\nDevelopment should be performed using `poetry <https://python-poetry.org/>`_ to handle\nthe development environment. Once poetry is installed, you can install the environment,\nwhich will include ``frispy``:\n\n.. code-block:: bash\n\n   poetry install\n\nAll proceeding instructions assume you entered your virtual environment using ``poetry shell``,\notherwise prepend ``poetry run`` to all instructions.\n\nIf you intend to open a pull request, please make sure ``pre-commit`` is installed\nbefore committing to your branch:\n\n.. code-block:: bash\n\n   pre-commit install\n\nThis will ensure that the code you submit is PEP8 compliant. Otherwise, CI checks will\nfail before merging can be completed.\n\nVerify your installation by running:\n\n.. code-block:: bash\n\n   pytest\n\nPlease report any problems you encounter on the `issues page\n<https://github.com/tmcclintock/FrisPy/issues>`_. Thank you!\n',
    'author': 'Tom McClintock',
    'author_email': 'thmsmcclintock@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
