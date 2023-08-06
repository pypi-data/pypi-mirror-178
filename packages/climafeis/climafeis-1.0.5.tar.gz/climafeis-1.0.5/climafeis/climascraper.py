import argparse
import os
from datetime import date
from enum import Enum

import bs4
import numpy as np
import pandas as pd
import requests


class Estacao(Enum):
    ILHA_SOLTEIRA = 1
    MARINOPOLIS = 2
    JUNQUEIROPOLIS = 3
    PARANAPUA = 4
    IRAPURU = 9
    POPULINA = 10
    SANTA_ADELIA_PIONEIROS = 11
    SANTA_ADELIA = 12
    BONANCA = 13
    ITAPURA = 14
    DRACENA = 19


def login(user, pw):
    url = 'http://clima.feis.unesp.br/valida.php'
    payload = {'usuario': user, 'senha': pw, 'enviar': 'Enviar'}

    s = requests.Session()
    s.post(url, data=payload)

    return s


# Fmt data: dd/MM/YYYY (03/06/2020)
def fetch_daily(session, dataini, datafim, estacao):
    url = 'http://clima.feis.unesp.br/recebe_formulario.php'
    payload = {'requireddataini': dataini, 'requireddatafim': datafim, 'estacao': estacao.value,
               'RadioGroup1': 'dados_diario', 'enviar': 'Enviar'}

    r = session.post(url, payload)
    soup = bs4.BeautifulSoup(r.content, 'html5lib')
    table_daily = soup.find_all('table')[1]
    try:
        df = parse_daily(table_daily.prettify())
    except Exception as e:
        print(f'[ERROR] Failed to parse HTML table: {e}')
        with open('response.html', 'wb') as f:
            f.write(r.content)
        return -1

    df.to_csv('planilha.csv')
    return 0


def parse_daily(daily_data):
    headers = {0: 'Tmedia', 1: 'Tmax', 2: 'Tmin',
               3: 'Urel_media', 4: 'Urel_max', 5: 'Urel_min',
               6: 'P_atm', 7: 'R_global', 8: 'R_liq', 9: 'Flux_calor',
               10: 'PAR', 11: 'Ev_tca', 12: 'ET0_pm', 13: 'ET0_tca', 14: 'Vvento_max',
               15: 'Vvento_media', 16: 'Dir_vento', 17: 'Chuva', 18: 'Insolacao'}
    headers = pd.Series(headers)

    dfs = pd.read_html(daily_data, index_col=0, parse_dates=True, flavor='html5lib')

    df = pd.concat(dfs, axis=1, sort=False, ignore_index=True)
    df = df[2:-11]
    df = df[[i for i in range(19)]]

    df = df.rename(columns=headers)
    df.index.name = 'Data'
    df = df.replace('-', np.nan)

    return df


def main():
    parser = argparse.ArgumentParser(description='Scrape dados diários do Canal CLIMA (http://clima.feis.unesp.br).')
    parser.add_argument('estacao', type=str,
                        help="""Nome da estação: ILHA_SOLTEIRA, MARINOPOLIS, JUNQUEIROPOLIS, PARANAPUA, IRAPURU, 
                        POPULINA, SANTA_ADELIA_PIONEIROS, SANTA_ADELIA, BONANCA, ITAPURA, DRACENA.""")
    parser.add_argument('dataInicial', type=str, help='Data inicial no formato dd/MM/YYYY (30/05/2020).')
    parser.add_argument('dataFinal', nargs='?', default=date.today().strftime('%d/%m/%Y'), type=str,
                        help='Data final no formato dd/MM/YYYY (03/05/2020). Padrão: presente dia.')
    parser.add_argument('-U', '--user', type=str,
                        help='Usuário do Canal CLIMA. Caso seu usuário não esteja em $USER_CLIMAFEIS.')
    parser.add_argument('-P', '--pw', type=str,
                        help='Senha do Canal CLIMA. Caso sua senha não esteja em $PASSWD_CLIMAFEIS.')
    args = parser.parse_args()
    if args.user or args.pw:
        s = login(args.user, args.pw)
    else:
        s = login(os.environ['USER_CLIMAFEIS'], os.environ['PASSWD_CLIMAFEIS'])

    fetch_daily(s, args.dataInicial, args.dataFinal, Estacao[args.estacao])


if __name__ == '__main__':
    main()
