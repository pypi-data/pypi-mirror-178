# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roc',
 'roc.dadi',
 'roc.dadi.config',
 'roc.dadi.tasks',
 'roc.dadi.tests',
 'roc.dadi.tools']

package_data = \
{'': ['*'], 'roc.dadi.tests': ['data-tasks/*']}

install_requires = \
['SQLAlchemy>=1.3,<2.0',
 'h5py>=3.7,<4.0',
 'maser-tools>=0.1.3',
 'pandas>=1.1.3',
 'poppy-core',
 'poppy-pop',
 'psycopg2>=2.8.4,<3.0.0',
 'roc-dingo>=1.0,<2.0',
 'spacepy>=0.4,<0.5',
 'xmltodict==0.13.0']

setup_kwargs = {
    'name': 'roc-dadi',
    'version': '0.3.4',
    'description': 'RPW DAta DIspatcher (DADI): Plugin to handle data files read/write by the pipeline',
    'long_description': 'DADI PLUGIN README\n===================\n\nINTRODUCTION\n-------------\n\nThis directory contains the source files of the RPW DAta DIspatcher (DADI), a plugin used to handle data files read/write by the RPW operation and data pipeline (RODP).\n\nDADI is not designed to be run as a stand-alone plugin, but with the RODP.\n\nDADI is developed with and run under the POPPY framework.\n\nCONTENT\n--------\n\n::\n\n    roc/                    plugin source files\n    .editorconfig           EditorConfig config file\n    .gitignore              .gitignore file\n    .gitlab-ci              config file for Gitlab-CI\n    .pre-commit-config.yaml pre-commit config file\n    bump_descriptor.py      Python script to synchronize roc/dadi/descriptor.json content with the pyproject.toml data\n    MANIFEST.in             Required to build Python package distributions\n    poetry.lock             Used by poetry package\n    pyproject.toml          pyproject.toml file (PEP518)\n    README.rst              present file\n    setup.py                setup.py (required for editable mode)\n\nHOWTO\n------\n\nHow to install the plugin?\n..........................\n\nThe plugin is designed to be installed and run inside a RODP instance.\nHowever it can be installed manually, by entering:\n\n.. code::\n\n    python -m pip install /path_to_plugin\n\nN.B. To install the plugin in editable mode, run the command:\n\n.. code::\n\n    python -m pip install -e /path_to_plugin\n\nThe editable mode can only used if the setup.py file exits. Use the dephell module to generate it from the pyproject.toml file (dephell deps convert).\n\nHow to release a new version of the plugin?\n...........................................................\n\n1. Update the version field in the :code:`pyproject.toml` file.\n\n2. Make sure the :code:`poetry.lock` file is up-to-date running: :code:`poetry update --lock`. (Use :code:`pip install poetry -U` to install poetry.)\n\n3. Update the descriptor file running the command: :code:`python bump_descriptor.py -m <message>`, where `<message>` must contain the change log for the new version.\n\n4. Commit last changes in the `develop` branch of Git repository. Merge `develop` branch into `master`. Create a new tag "X.Y.Z" from `master` branch. Rebase `master` onto `develop`. Push `master`, `develop` and the new tag in the distant server.\n\nHow to call the plugin?\n..........................\n\nThe plugin can only by called from a POPPy-like pipeline (e.g, RODP).\n\nThe main command is:\n\n.. code::\n\n    python manage.py dadi\n\n.. note::\n\n    * The :code:`manage.py` file is inside the pipeline root directory (depending of the pipeline installation the alias :code:`pop` can be also used).\n    * The command below will return the help message by default if no sub-command is passed\n',
    'author': 'Xavier Bonnin',
    'author_email': 'xavier.bonnin@obspm.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.obspm.fr/ROC/Pipelines/Plugins/DADI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
