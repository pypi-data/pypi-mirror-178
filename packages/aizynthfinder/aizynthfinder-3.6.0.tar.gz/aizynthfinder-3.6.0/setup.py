# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aizynthfinder',
 'aizynthfinder.analysis',
 'aizynthfinder.chem',
 'aizynthfinder.context',
 'aizynthfinder.context.cost',
 'aizynthfinder.context.policy',
 'aizynthfinder.context.scoring',
 'aizynthfinder.context.stock',
 'aizynthfinder.interfaces',
 'aizynthfinder.interfaces.gui',
 'aizynthfinder.search',
 'aizynthfinder.search.breadth_first',
 'aizynthfinder.search.dfpn',
 'aizynthfinder.search.mcts',
 'aizynthfinder.search.retrostar',
 'aizynthfinder.tools',
 'aizynthfinder.training',
 'aizynthfinder.utils']

package_data = \
{'': ['*'], 'aizynthfinder': ['data/*', 'data/templates/*']}

install_requires = \
['deprecated>=1.2.10,<2.0.0',
 'ipywidgets>=7.5.1,<8.0.0',
 'jinja2>=3.0.0,<4.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'jupytext>=1.3.3,<2.0.0',
 'more-itertools>=8.2.0,<9.0.0',
 'networkx>=2.4,<3.0',
 'pandas>=1.0.0,<2.0.0',
 'pillow>=9.0.0,<10.0.0',
 'rdchiral>=1.0.0,<2.0.0',
 'rdkit>=2022.3.3,<2023.0.0',
 'requests>=2.23.0,<3.0.0',
 'tables>=3.6.1,<4.0.0',
 'tensorflow>=2.8.0,<3.0.0',
 'tqdm>=4.42.1,<5.0.0']

extras_require = \
{'all': ['grpcio>=1.24.0,<2.0.0',
         'tensorflow-serving-api>=2.1.0,<3.0.0',
         'pymongo>=3.10.1,<4.0.0',
         'route-distances>=1.1.0,<2.0.0',
         'scipy>=1.0,<2.0',
         'matplotlib>=3.0.0,<4.0.0',
         'timeout-decorator>=0.5.0,<0.6.0']}

entry_points = \
{'console_scripts': ['aizynthapp = aizynthfinder.interfaces.aizynthapp:main',
                     'aizynthcli = aizynthfinder.interfaces.aizynthcli:main',
                     'cat_aizynth_output = aizynthfinder.tools.cat_output:main',
                     'download_public_data = '
                     'aizynthfinder.tools.download_public_data:main',
                     'smiles2stock = aizynthfinder.tools.make_stock:main']}

setup_kwargs = {
    'name': 'aizynthfinder',
    'version': '3.6.0',
    'description': 'Retrosynthetic route finding using neural network guided Monte-Carlo tree search',
    'long_description': '# AiZynthFinder \n\n[![License](https://img.shields.io/github/license/MolecularAI/aizynthfinder)](https://github.com/MolecularAI/aizynthfinder/blob/master/LICENSE)\n[![Tests](https://github.com/MolecularAI/aizynthfinder/workflows/tests/badge.svg)](https://github.com/MolecularAI/aizynthfinder/actions?workflow=tests)\n[![codecov](https://codecov.io/gh/MolecularAI/aizynthfinder/branch/master/graph/badge.svg)](https://codecov.io/gh/MolecularAI/aizynthfinder)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black) \n[![version](https://img.shields.io/github/v/release/MolecularAI/aizynthfinder)](https://github.com/MolecularAI/aizynthfinder/releases)\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MolecularAI/aizynthfinder/blob/master/contrib/notebook.ipynb)\n\n\nAiZynthFinder is a tool for retrosynthetic planning. The algorithm is based on a Monte Carlo tree search that recursively breaks down a molecule to purchasable precursors. The tree search is guided by a policy that suggests possible precursors by utilizing a neural network trained on a library of known reaction templates.\n\nAn introduction video can be found here: [https://youtu.be/r9Dsxm-mcgA](https://youtu.be/r9Dsxm-mcgA)\n\n## Prerequisites\n\nBefore you begin, ensure you have met the following requirements:\n\n* Linux, Windows or macOS platforms are supported - as long as the dependencies are supported on these platforms.\n\n* You have installed [anaconda](https://www.anaconda.com/) or [miniconda](https://docs.conda.io/en/latest/miniconda.html) with python 3.8 - 3.9\n\nThe tool has been developed on a Linux platform, but the software has been tested on Windows 10 and macOS Catalina.\n\n\n## Installation\n\n### For end-users\n\nFirst time, execute the following command in a console or an Anaconda prompt\n\n    conda create "python>=3.8,<3.10" -n aizynth-env\n    \nTo install, activate the environment and install the package using pypi\n\n    conda activate aizynth-env\n    python -m pip install aizynthfinder[all]\n\nfor a smaller package, without all the functionality, you can also type\n\n    python -m pip install aizynthfinder\n\n### For developers\n\nFirst clone the repository using Git.\n\nThen execute the following commands in the root of the repository \n\n    conda env create -f env-dev.yml\n    conda activate aizynth-dev\n    poetry install -E all\n    \nthe `aizynthfinder` package is now installed in editable mode.\n\n## Usage\n\nThe tool will install the ``aizynthcli`` and ``aizynthapp`` tools\nas interfaces to the algorithm:\n\n```\naizynthcli --config config.yml --smiles smiles.txt\naizynthapp --config config.yml\n```\n\nConsult the documentation [here](https://molecularai.github.io/aizynthfinder/) for more information.\n\nTo use the tool you need\n\n    1. A stock file\n    2. A trained rollout policy network (including the Keras model and the list of unique templates)\n    3. A trained filer policy network (optional)\n\nSuch files can be downloaded from [figshare](https://figshare.com/articles/AiZynthFinder_a_fast_robust_and_flexible_open-source_software_for_retrosynthetic_planning/12334577) and [here](https://figshare.com/articles/dataset/A_quick_policy_to_filter_reactions_based_on_feasibility_in_AI-guided_retrosynthetic_planning/13280507) or they can be downloaded automatically using\n\n```\ndownload_public_data my_folder\n```\n\nwhere ``my_folder`` is the folder that you want download to.\nThis will create a ``config.yml`` file that you can use with either ``aizynthcli`` or ``aizynthapp``.\n\n## Development\n\n### Testing\n\nTests uses the ``pytest`` package, and is installed by `poetry`\n\nRun the tests using:\n\n    pytest -v\n\nThe full command run on the CI server is available through an `invoke` command\n\n    invoke full-tests\n    \n ### Documentation generation\n\nThe documentation is generated by Sphinx from hand-written tutorials and docstrings\n\nThe HTML documentation can be generated by\n\n    invoke build-docs\n\n## Contributing\n\nWe welcome contributions, in the form of issues or pull requests.\n\nIf you have a question or want to report a bug, please submit an issue.\n\n\nTo contribute with code to the project, follow these steps:\n\n1. Fork this repository.\n2. Create a branch: `git checkout -b <branch_name>`.\n3. Make your changes and commit them: `git commit -m \'<commit_message>\'`\n4. Push to the remote branch: `git push`\n5. Create the pull request.\n\nPlease use ``black`` package for formatting, and follow ``pep8`` style guide.\n\n\n## Contributors\n\n* [@SGenheden](https://www.github.com/SGenheden)\n* [@EBjerrum](https://www.github.com/EBjerrum)\n* [@A-Thakkar](https://www.github.com/A-Thakkar)\n* [@benteb](https://www.github.com/benteb)\n\nThe contributors have limited time for support questions, but please do not hesitate to submit an issue (see above).\n\n## License\n\nThe software is licensed under the MIT license (see LICENSE file), and is free and provided as-is.\n\n## References\n\n1. Thakkar A, Kogej T, Reymond J-L, et al (2019) Datasets and their influence on the development of computer assisted synthesis planning tools in the pharmaceutical domain. Chem Sci. https://doi.org/10.1039/C9SC04944D\n2. Genheden S, Thakkar A, Chadimova V, et al (2020) AiZynthFinder: a fast, robust and flexible open-source software for retrosynthetic planning. J. Cheminf. https://jcheminf.biomedcentral.com/articles/10.1186/s13321-020-00472-1\n3. Genheden S, Engkvist O, Bjerrum E (2020) A Quick Policy to Filter Reactions Based on Feasibility in AI-Guided Retrosynthetic Planning. ChemRxiv. Preprint. https://doi.org/10.26434/chemrxiv.13280495.v1 \n4. Genheden S, Engkvist O, Bjerrum E (2021) Clustering of synthetic routes using tree edit distance. J. Chem. Inf. Model. 61:3899–3907 [https://doi.org/10.1021/acs.jcim.1c00232](https://doi.org/10.1021/acs.jcim.1c00232)\n5. Genheden S, Engkvist O, Bjerrum E (2022) Fast prediction of distances between synthetic routes with deep learning. Mach. Learn. Sci. Technol. 3:015018 [https://doi.org/10.1088/2632-2153/ac4a91](https://doi.org/10.1088/2632-2153/ac4a91) \n',
    'author': 'Molecular AI group',
    'author_email': 'samuel.genheden@astrazeneca.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MolecularAI/aizynthfinder/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
