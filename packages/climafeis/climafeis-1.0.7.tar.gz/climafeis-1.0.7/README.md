# climafeis
Script CLI em Python para scrape do banco de dados climatológicos do [Canal CLIMA](https://clima.feis.unesp.br) da [UNESP Ilha Solteira](https://www.feis.unesp.br/) com a biblioteca [Requests](https://requests.readthedocs.io/en/latest/).  

### Installation
1. Certifique-se que o Python 3.8 ou superior e o pip estejam instalados
1. Rode `pip install climafeis`

### Development
1. Confira sua versão do Python com `python -V`
1. Instale o Python 3.8 ou superior e pip, caso já não estejam instalados:

    - Windows `winget install Python.Python.3.X` (substitua X com a minor version desejada)
    - Ubuntu e derivados `apt install python3 python3-pip`
    - Arch e derivados `pacman -S python python-pip`
    - Fedora `dnf install python3 python3-pip`

1. [Instale o poetry](https://python-poetry.org/docs/#installation) 
1. Clone esse repositório com `git clone https://github.com/joaofauvel/climafeis.git && cd climafeis`
1. Instale os requisitos `poetry install`

### Output headers
| Header     | Description                                           |
| ---------- | ----------------------------------------------------- |
| Date       | Observation date (dd-mm-yyyy)                         |
| Tmean      | Mean temperature (ºC)                                 |
| Tmax       | Max temperature (ºC)                                  |
| Tmin       | Min temperature (ºC)                                  |
| RHmean     | Mean relative humidity (%)                            |
| RHmax      | Max relative humidity (%)                             |
| RHmin      | Min relative humidity (%)                             |
| Pmean      | Mean pressure (kPa)                                   |
| Rn         | Net radiation (MJ/m^2*day)                            |
| Rl         | Liquid radiation (MJ/m^2*day)                         |
| G          | Soil heat flux (MJ/m^2*day)                           |
| PAR        | (μmoles/m^2)                                          |
| ETcat      | Evapotranspiration Class A Tank (mm/day)              |
| ET0pm      | Reference evapotranspiration Penman–Monteith (mm/day) |
| ET0cat     | Reference evapotranspiration Class A Tank (mm/day)    |
| U2max      | Max windspeed at 2 meters (m/s)                       |
| U2mean     | Mean windspeed at 2 meters (m/s)                      |
| U2dir      | Wind direction at 2 meters (º)                        |
| Rain       | Rainfall (mm)                                         |
| Insolation | Solar insolation (h/day)                              |

### Usage
    usage: climafeis [-h] [-U USER] [-P PW] [-o OUT] [-l LOG] [-v] station start [end]

    Scrape daily climate date from Canal CLIMA (https://clima.feis.unesp.br)

    positional arguments:
    station               station name: ILHA_SOLTEIRA, MARINOPOLIS, JUNQUEIROPOLIS, PARANAPUA, IRAPURU, POPULINA,
                            SANTA_ADELIA_PIONEIROS, SANTA_ADELIA, BONANCA, ITAPURA, DRACENA
    start                 start date dd/MM/YYYY (30/05/2020)
    end                   end date dd/MM/YYYY (03/05/2020). Default: today

    options:
    -h, --help            show this help message and exit
    -U USER, --user USER  override Canal CLIMA user set in the environment variable $USER_CLIMAFEIS
    -P PW, --pw PW        override Canal CLIMA password set in the environment variable $PASSWD_CLIMAFEIS
    -o OUT, --output OUT  output file. Default: <station>.csv
    -l LOG, --log LOG     output log file. Default: stdout
    -v, --verbose


