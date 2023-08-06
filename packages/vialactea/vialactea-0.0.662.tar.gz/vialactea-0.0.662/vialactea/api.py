import json
from pprint import pp
from time import sleep

import mysql.connector as msql
import pandas as pd
import requests
from colorama import init, Style, Back, Fore
from mysql.connector import errorcode
from progress.bar import Bar

init(autoreset=True)


def db_connect():
    _login_params = input('Please insert your login file path: ')

    with open(_login_params, 'r', encoding='utf8') as _lp:
        login_params = json.load(_lp)

    try:
        conn = msql.connect(
            host=login_params['host'],
            user=login_params['user'],
            password=login_params['password'],
            database=login_params['database']
        )

        if conn.is_connected():
            print('Nice DB Login')
            return conn

    except msql.Error as err:
        if err.errno == errorcode.ER_ACCES_DENIED_ERROR:
            pp('Bad Login. Check user, pass params')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            pp('Schema does not exist')
        else:
            pp(err)


def getCols(schema_table):
    querry = f'SHOW COLUMNS FROM {schema_table}'
    with db_connect() as con:
        # *--Abrindo conexão, criando o cursor e executando o comando
        c = con.cursor()
        try:
            c.execute(querry)
            print(f'[Querry executed {schema_table}]')
        except Exception as e:
            print('[Something went wrong]')
            print(f'[Bad execution select {schema_table}]')
            print(f'[{e}]')

        resposta = c.fetchall()
    return [item[0] for item in resposta]


def table_truncate(schema_table):
    querry = f'TRUNCATE TABLE {schema_table}'
    with db_connect() as con:
        # *--Abrindo conexão, criando o cursor e executando o comando
        c = con.cursor()
        try:
            c.execute(querry)
            print(f'[{schema_table} was nicely truncated]')
        except Exception as e:
            print('[Something went wrong]')
            print(f'[Bad execution at Truncate in {schema_table}]')
            print(f'[{e}]')


def table_refresh(schema_table, arg):
    _param = ''
    querry = f'DELETE FROM {schema_table} WHERE dataEmissao > "{arg}"'
    with db_connect() as con:
        # *--Abrindo conexão, criando o cursor e executando o comando
        c = con.cursor()
        try:
            c.execute(querry)
            con.commit()
            print()
            print(
                f'[Success at drop rows from {schema_table} using {arg} parameter, {c.rowcount} afected]')
        except Exception as e:
            print('[Something went wrong]')
            print(f'[Bad execution to Delte rows in {schema_table}]')
            print(f'[{e}]')


def insert_payload(table, response_dataframe):
    try:
        sstr = '%s'
        cols = getCols(schema_table=table)
        insert_dict = {key: '0' for key in cols}
        default_dict = {}
        querry = '''
        INSERT INTO %s
        (%s)
        VALUES (%s)
        ''' % (
            table,
            ''.join(f'{cols[i]}' if cols[i] == cols[-1]
                    else f'{cols[i]},' for i in range(len(cols))),
            ''.join(sstr if cols[i] == cols[-1]
                    else f'{sstr},' for i in range(len(cols)))
        )
        df = response_dataframe
        df.columns = df.columns.str.replace('.', '')
        df.columns = df.columns.str.replace(' ', '')
        size_df = len(df)
        with db_connect() as con:
            c = con.cursor()
            with Bar(f'Load insert from file', max=size_df) as bar:
                for line in range(size_df):
                    temp_dict = df.loc[line].to_dict()
                    for key in insert_dict:
                        try:
                            default_dict[key] = temp_dict[f'{key}']
                        except:
                            default_dict[key] = insert_dict[key]
                    c.execute(querry, list(default_dict.values()))
                    con.commit()
                    bar.next()
    except Exception as e:
        pp('Something went wrong')
        pp(e)
        sleep(5)


def notasfiscais():
    situacao = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    tipo = ['e', 's']
    request_list = []
    for comp in COMP:
        for _tipo in tipo:
            for cur_situ in situacao:
                payload = {
                    'apikey': KEYS.loc[comp, 'val'],
                    'filters': f"{API_CFG['bling']['bling_notasfiscais']['params']['dhEmi']};situacao[{cur_situ}];tipo[{_tipo}]"
                }
                pag = 1
                while true:
                    r = requests.get(
                        url=f'{API_CFG["bling"]["bling_notasfiscais"]["link"]}/page={pag}/json', params=payload)
                    sleep(0.5)
                    try:
                        c = r.json()['retorno']['erros']
                        print(Style.NORMAL + Back.WHITE + Fore.YELLOW + f'[{comp}] {c}')
                        if c is not None:
                            break
                    except:
                        resposta = r.json()['retorno']
                        resposta['empresa'] = comp
                        request_list.append(resposta)
                        print(Style.NORMAL + Back.CYAN + Fore.WHITE +
                              f'[{comp}] [{API_CFG["bling"]["bling_notasfiscais"]["situacoes_alias"][int(cur_situ)]}, type: {_tipo}, page: {pag} sent to list.]')
                        pass
                    pag += 1
    return request_list


def contasreceber():
    situacao = ['pago', 'cancelada', 'aberto', 'parcial']
    request_list = []
    for comp in COMP:
        for cur_situ in situacao:
            payload = {
                'apikey': KEYS.loc[comp, 'val'],
                'filters': f"{API_CFG['bling']['bling_contasreceber']['params']['dhEmi']};situacao[{cur_situ}]"
            }
            pag = 1
            while true:
                r = requests.get(
                    url=f'{API_CFG["bling"]["bling_contasreceber"]["link"]}/page={pag}/json', params=payload)
                sleep(0.5)
                try:
                    c = r.json()['retorno']['erros']
                    print(Style.NORMAL + Back.WHITE + Fore.YELLOW + f'[{comp}] {c}')
                    if c is not None:
                        break
                except:
                    resposta = r.json()['retorno']
                    resposta['empresa'] = comp
                    request_list.append(resposta)
                    print(Style.NORMAL + Back.CYAN + Fore.WHITE + f'[{comp}] [{cur_situ}, page: {pag} sent to list.]')
                    pass
                pag += 1
    return request_list


def tabular_list(request_list):
    # ? l é associao à uma lista
    l = request_list
    # ? esta lista vazia se torna uma lista de dicionários
    df = []
    # ? para índice da lista
    for i in l:
        _key = list(i.keys())[0]
        _comp = list(i.keys())[1]
        for item in i[_key]:
            _nkey = list(item.keys())[0]
            item[_nkey]['empresa'] = i[_comp]
            df.append(item[_nkey])
    # ? laço para descomprimir o campo de clientes de cada dicionário da lista
    for _dict in df:

        _dict['_id'] = _dict['id']
        for key in _dict['cliente']:
            _dict[f'cli{key}'] = _dict['cliente'][key]
        _dict.pop('cliente')
        _dict.pop('id')
    d = pd.DataFrame(df)
    d = d.fillna('')
    d = d.astype('str')
    return d
