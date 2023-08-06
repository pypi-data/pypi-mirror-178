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
    'version': '1.0.8',
    'description': 'CLI Python application for scraping daily climate data from Canal CLIMA using requests and BeautifulSoup 4.',
    'long_description': "# climafeis\nCLI Python application for scraping daily climate data from [Canal CLIMA](https://clima.feis.unesp.br) [UNESP Ilha Solteira](https://www.feis.unesp.br/) using [requests](https://requests.readthedocs.io/en/latest/) and [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/).  \n\n### Installation\n1. Make sure Python 3.8 or higher and pip are installed\n1. Run `pip install climafeis`\n\n### Development\n1. Check Python's version `python -V`\n1. Install Python 3.8 or higher and pip, if they aren't already installed:\n\n    - Windows `winget install Python.Python.3.X` (replace X with the desired minor version)\n    - Ubuntu based distros `apt install python3 python3-pip`\n    - Arch based distros `pacman -S python python-pip`\n    - Fedora `dnf install python3 python3-pip`\n\n1. [Install poetry](https://python-poetry.org/docs/#installation) \n1. Clone this repo `git clone https://github.com/joaofauvel/climafeis.git && cd climafeis`\n1. Install requirements `poetry install`\n\n### Output headers\n| Header     | Description                                           |\n| ---------- | ----------------------------------------------------- |\n| Date       | Observation date (dd-mm-yyyy)                         |\n| Tmean      | Mean temperature (ºC)                                 |\n| Tmax       | Max temperature (ºC)                                  |\n| Tmin       | Min temperature (ºC)                                  |\n| RHmean     | Mean relative humidity (%)                            |\n| RHmax      | Max relative humidity (%)                             |\n| RHmin      | Min relative humidity (%)                             |\n| Pmean      | Mean pressure (kPa)                                   |\n| Rn         | Net radiation (MJ/m^2*day)                            |\n| Rl         | Liquid radiation (MJ/m^2*day)                         |\n| G          | Soil heat flux (MJ/m^2*day)                           |\n| PAR        | (μmoles/m^2)                                          |\n| ETcat      | Evapotranspiration Class A Tank (mm/day)              |\n| ET0pm      | Reference evapotranspiration Penman–Monteith (mm/day) |\n| ET0cat     | Reference evapotranspiration Class A Tank (mm/day)    |\n| U2max      | Max windspeed at 2 meters (m/s)                       |\n| U2mean     | Mean windspeed at 2 meters (m/s)                      |\n| U2dir      | Wind direction at 2 meters (º)                        |\n| Rain       | Rainfall (mm)                                         |\n| Insolation | Solar insolation (h/day)                              |\n[Reference](https://www.fao.org/3/x0490e/x0490e06.htm)\n\n### Usage\nDaily data from ILHA_SOLTEIRA station from 30/05/2020 (dd/MM/YYYY) to 03/05/2020  \n`climafeis ILHA_SOLTEIRA 30/05/2020 03/06/2020`\n\nDaily data from MARINOPOLIS station from 30/05/2020 to today  \n`climafeis MARINOPOLIS 30/05/2020`\n\nDaily data from ILHA_SOLTEIRA station from 30/05/2020 to today, supplying username and password  \n`climafeis ILHA_SOLTEIRA 30/05/2020 -U user -P password`  \n\n---\n\n    usage: climafeis [-h] [-U USER] [-P PW] [-o OUT] [-l LOG] [-v] station start [end]\n\n    Scrape daily climate date from Canal CLIMA (https://clima.feis.unesp.br)\n\n    positional arguments:\n    station               station name: ILHA_SOLTEIRA, MARINOPOLIS, JUNQUEIROPOLIS, PARANAPUA, IRAPURU, \n                            POPULINA, SANTA_ADELIA_PIONEIROS, SANTA_ADELIA, BONANCA, ITAPURA, DRACENA\n    start                 start date dd/MM/YYYY (30/05/2020)\n    end                   end date dd/MM/YYYY (03/05/2020). Default: today\n\n    options:\n    -h, --help            show this help message and exit\n    -U USER, --user USER  override Canal CLIMA user set in the environment variable $USER_CLIMAFEIS\n    -P PW, --pw PW        override Canal CLIMA password set in the environment variable $PASSWD_CLIMAFEIS\n    -o OUT, --output OUT  output file. Default: <station>.csv\n    -l LOG, --log LOG     output log file. Default: stdout\n    -v, --verbose\n",
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
