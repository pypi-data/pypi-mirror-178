# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['climafeis']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'html5lib>=1.1,<2.0',
 'numpy>=1.23.5,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['climafeis = climafeis.climascraper:main']}

setup_kwargs = {
    'name': 'climafeis',
    'version': '1.0.5',
    'description': 'Scrape dados climáticos de clima.feis.unesp.br',
    'long_description': '# climafeis\nScript CLI em Python para scrape do banco de dados climatológicos do [Canal CLIMA](http://clima.feis.unesp.br) da [UNESP Ilha Solteira](https://www.feis.unesp.br/) com a biblioteca [Requests](https://requests.readthedocs.io/en/latest/).  \n\n### Instalação\n1. Certifique-se que o Python 3.8 ou superior e o pip estejam instalados\n1. Rode `pip install climafeis`\n\n### Instalação para desenvolvimento\n1. Confira sua versão do Python com `python -V`\n1. Instale o Python 3.8 ou superior e pip, caso já não estejam instalados:\n\n    - Windows `winget install Python.Python.3.X` (substitua X com a minor version desejada)\n    - Ubuntu e derivados `apt install python3 python3-pip`\n    - Arch e derivados `pacman -S python python-pip`\n    - Fedora `dnf install python3 python3-pip`\n\n1. [Instale o poetry](https://python-poetry.org/docs/#installation) \n1. Clone esse repositório com `git clone https://github.com/joaofauvel/climafeis.git && cd climafeis`\n1. Instale os requisitos `poetry install`\n\n### Utilização\n    usage: climafeis [-h] [-U USER] [-P PW] estacao dataInicial [dataFinal]\n\n    Scrape dados diários do Canal CLIMA (http://clima.feis.unesp.br).\n\n    positional arguments:\n        estacao               Nome da estação: ILHA_SOLTEIRA, MARINOPOLIS, JUNQUEIROPOLIS, PARANAPUA,\n        IRAPURU, POPULINA, SANTA_ADELIA_PIONEIROS, SANTA_ADELIA, BONANCA, ITAPURA, DRACENA.\n        \n        dataInicial           Data inicial no formato dd/MM/YYYY (30/05/2020).\n        dataFinal             Data final no formato dd/MM/YYYY (03/05/2020). Padrão: presente dia.\n\n    optional arguments:\n        -h, --help            show this help message and exit\n        -U USER, --user USER  Usuário do Canal CLIMA. Caso seu usuário não esteja em $USER_CLIMAFEIS.\n        -P PW, --pw PW        Senha do Canal CLIMA. Caso sua senha não esteja em $PASSWD_CLIMAFEIS.\n        \n    Exemplos:\n        climafeis ILHA_SOLTEIRA 30/05/2020 03/06/2020             Extraí dados diários da estação de Ilha\n        Solteira dos dias 30/05/2020 ao dia 03/05/2020\n        \n        climafeis MARINOPOLIS 30/05/2020                          Extraí dados diários da estação de\n        Marinópolis dos dias 30/05/2020 ao presente dia\n        \n        climafeis ILHA_SOLTEIRA 30/05/2020 -U usuário -P senha    \n\n\n',
    'author': 'João Fauvel',
    'author_email': 'jmmfauvel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/joaofauvel/climafeis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
