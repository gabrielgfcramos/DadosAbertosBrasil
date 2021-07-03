'''Módulo para consulta a informações variadas.

Essas funções são importadas pelo `__init__` do super-módulo
`DadosAbertosBrasil`.

Elas consistem em informações diversas ou em funções pré-parametrizadas de
outros módulo. Seu objetivo é facilitar o acesso às informações de maior
interesse público.

'''
import pandas as _pd
import requests

from ._utils import parse
from . import bacen
from . import ipea



def catalogo() -> _pd.DataFrame:
    '''Catálogo de iniciativas oficiais de dados abertos no Brasil.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo um catálogo de iniciativas de dados abertos.

    Créditos
    --------
    https://github.com/dadosgovbr

    Exemplos
    --------
    >>> favoritos.catalogo()
                                                   Título  \
    0                      Alagoas em dados e informações  \
    1                             Fortaleza Dados Abertos  \
    2                              Dados abertos – TCM-CE  \
    3                      Dados abertos Distrito Federal  \
    4                       Dados abertos – Governo do ES  \
    ..                                                ...  \

    '''

    URL = 'https://raw.githubusercontent.com/dadosgovbr/catalogos-dados-brasil/master/dados/catalogos.csv'
    return _pd.read_csv(URL)



def geojson(uf:str) -> dict:
    '''Coordenadas dos municípios brasileiros em formato GeoJSON para criação
    de mapas.

    Parâmetros
    ----------
    uf : str
        Nome ou sigla da Unidade Federativa.

    Retorna
    -------
    dict
        Coordenadas em formato .GeoJSON da UF pesquisada.

    Erros
    -----
    DAB_UFError
        Caso seja inserida uma UF inválida.

    Créditos
    --------
    https://github.com/tbrugz

    Exemplos
    --------
    >>> favoritos.geojson('SC')
    {
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'properties': {
                'id': '4200051',
                'name': 'Abdon Batista',
                'description': 'Abdon Batista'
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[
                    [-51.0378352721, -27.5044338231],
                    [-51.0307859254, -27.5196681175],
                    [-51.0175689993, -27.5309862449],
                    [-50.9902859975, -27.5334223314],
                    [-50.9858971419, -27.5302011257],
                    ...

    '''

    uf = parse.uf(uf)
    
    mapping = {

        'BR': 100,

        'AC': 12,
        'AM': 13,
        'AP': 16,
        'PA': 15,
        'RO': 11,
        'RR': 14,
        'TO': 17,

        'AL': 27,
        'BA': 29,
        'CE': 23,
        'MA': 21,
        'PB': 25,
        'PE': 26,
        'PI': 22,
        'RN': 24,
        'SE': 28,

        'ES': 32,
        'MG': 31,
        'RJ': 33,
        'SP': 35,

        'PR': 41,
        'RS': 43,
        'SC': 42,

        'DF': 53,
        'GO': 52,
        'MT': 51,
        'MS': 50

    }
    
    url = f'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-{mapping[uf]}-mun.json'
    return requests.get(url).json()



def codigos_municipios() -> _pd.DataFrame:
    '''Lista dos códigos dos municípios do IBGE e do TSE.
    Utilizado para correlacionar dados das duas APIs diferentes.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo os códigos do IBGE e do TSE para todos os
        municípios do Brasil.

    Créditos
    --------
    https://github.com/betafcc

    Exemplos
    --------
    >>> favoritos.codigos_municipios()
          codigo_tse  codigo_ibge nome_municipio  uf  capital
    0           1120      1200013     ACRELÂNDIA  AC        0
    1           1570      1200054   ASSIS BRASIL  AC        0
    2           1058      1200104      BRASILÉIA  AC        0
    3           1007      1200138         BUJARI  AC        0
    4           1015      1200179       CAPIXABA  AC        0
    ..           ...          ...            ...  ..      ...

    '''

    URL = r'https://raw.githubusercontent.com/betafcc/Municipios-Brasileiros-TSE/master/municipios_brasileiros_tse.json'
    df = _pd.read_json(URL)
    return df[['codigo_tse', 'codigo_ibge', 'nome_municipio', 'uf', 'capital']]



def perfil_eleitorado() -> _pd.DataFrame:
    '''Tabela com perfil do eleitorado por município.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo o perfil do eleitorado em todos os municípios.

    Exemplos
    --------
    >>> favoritos.perfil_eleitorado()
          NR_ANO_ELEICAO  CD_PAIS NM_PAIS SG_REGIAO NM_REGIAO SG_UF     NM_UF  \
    0               2020        1  Brasil         N     Norte    AC      Acre  \
    1               2020        1  Brasil         N     Norte    AC      Acre  \
    ..               ...      ...     ...       ...       ...   ...       ...  \

    '''

    return _pd.read_csv(
        r'https://raw.githubusercontent.com/GusFurtado/DadosAbertosBrasil/master/data/Eleitorado.csv',
        encoding = 'latin-1',
        sep = ';'
    )



def bandeira(uf:str, tamanho:int=100) -> str:
    '''Gera a URL da WikiMedia para a bandeira de um estado de um tamanho
    escolhido.

    Parâmetros
    ----------
    uf : str
        Sigla da Unidade Federativa.
    tamanho : int (default=100)
        Tamanho em pixels da bandeira.

    Retorna
    -------
    str
        URL da bandeira do estado no formato PNG.

    Erros
    -----
    DAB_UFError
        Caso seja inserida uma UF inválida.

    Exemplos
    --------
    Gera o link para uma imagem da bandeira de Santa Catarina de 200 pixels.

    >>> favoritos.bandeira(uf='SC', tamanho=200)
    'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/' ...

    '''
    
    URL = r'https://upload.wikimedia.org/wikipedia/commons/thumb/'
    
    bandeira = {
        'BR': f'0/05/Flag_of_Brazil.svg/{tamanho}px-Flag_of_Brazil.svg.png',
        'AC': f'4/4c/Bandeira_do_Acre.svg/{tamanho}px-Bandeira_do_Acre.svg.png',
        'AM': f'6/6b/Bandeira_do_Amazonas.svg/{tamanho}px-Bandeira_do_Amazonas.svg.png',
        'AL': f'8/88/Bandeira_de_Alagoas.svg/{tamanho}px-Bandeira_de_Alagoas.svg.png',
        'AP': f'0/0c/Bandeira_do_Amap%C3%A1.svg/{tamanho}px-Bandeira_do_Amap%C3%A1.svg.png',
        'BA': f'2/28/Bandeira_da_Bahia.svg/{tamanho}px-Bandeira_da_Bahia.svg.png',
        'CE': f'2/2e/Bandeira_do_Cear%C3%A1.svg/{tamanho}px-Bandeira_do_Cear%C3%A1.svg.png',
        'DF': f'3/3c/Bandeira_do_Distrito_Federal_%28Brasil%29.svg/{tamanho}px-Bandeira_do_Distrito_Federal_%28Brasil%29.svg.png',
        'ES': f'4/43/Bandeira_do_Esp%C3%ADrito_Santo.svg/{tamanho}px-Bandeira_do_Esp%C3%ADrito_Santo.svg.png',
        'GO': f'b/be/Flag_of_Goi%C3%A1s.svg/{tamanho}px-Flag_of_Goi%C3%A1s.svg.png',
        'MA': f'4/45/Bandeira_do_Maranh%C3%A3o.svg/{tamanho}px-Bandeira_do_Maranh%C3%A3o.svg.png',
        'MG': f'f/f4/Bandeira_de_Minas_Gerais.svg/{tamanho}px-Bandeira_de_Minas_Gerais.svg.png',
        'MT': f'0/0b/Bandeira_de_Mato_Grosso.svg/{tamanho}px-Bandeira_de_Mato_Grosso.svg.png',
        'MS': f'6/64/Bandeira_de_Mato_Grosso_do_Sul.svg/{tamanho}px-Bandeira_de_Mato_Grosso_do_Sul.svg.png',
        'PA': f'0/02/Bandeira_do_Par%C3%A1.svg/{tamanho}px-Bandeira_do_Par%C3%A1.svg.png',
        'PB': f'b/bb/Bandeira_da_Para%C3%ADba.svg/{tamanho}px-Bandeira_da_Para%C3%ADba.svg.png',
        'PE': f'5/59/Bandeira_de_Pernambuco.svg/{tamanho}px-Bandeira_de_Pernambuco.svg.png',
        'PI': f'3/33/Bandeira_do_Piau%C3%AD.svg/{tamanho}px-Bandeira_do_Piau%C3%AD.svg.png',
        'PR': f'9/93/Bandeira_do_Paran%C3%A1.svg/{tamanho}px-Bandeira_do_Paran%C3%A1.svg.png',
        'RJ': f'7/73/Bandeira_do_estado_do_Rio_de_Janeiro.svg/{tamanho}px-Bandeira_do_estado_do_Rio_de_Janeiro.svg.png',
        'RO': f'f/fa/Bandeira_de_Rond%C3%B4nia.svg/{tamanho}px-Bandeira_de_Rond%C3%B4nia.svg.png',
        'RN': f'3/30/Bandeira_do_Rio_Grande_do_Norte.svg/{tamanho}px-Bandeira_do_Rio_Grande_do_Norte.svg.png',        
        'RR': f'9/98/Bandeira_de_Roraima.svg/{tamanho}px-Bandeira_de_Roraima.svg.png',
        'RS': f'6/63/Bandeira_do_Rio_Grande_do_Sul.svg/{tamanho}px-Bandeira_do_Rio_Grande_do_Sul.svg.png',
        'SC': f'1/1a/Bandeira_de_Santa_Catarina.svg/{tamanho}px-Bandeira_de_Santa_Catarina.svg.png',
        'SE': f'b/be/Bandeira_de_Sergipe.svg/{tamanho}px-Bandeira_de_Sergipe.svg.png',
        'SP': f'2/2b/Bandeira_do_estado_de_S%C3%A3o_Paulo.svg/{tamanho}px-Bandeira_do_estado_de_S%C3%A3o_Paulo.svg.png',
        'TO': f'f/ff/Bandeira_do_Tocantins.svg/{tamanho}px-Bandeira_do_Tocantins.svg.png',

        # Extintos
        'FN': f'3/3b/Fernando_de_Noronha%2C_PE_-_Bandeira.svg/{tamanho}px-Fernando_de_Noronha%2C_PE_-_Bandeira.svg.png',
        'GB': f'c/c3/Bandeira_do_Estado_da_Guanabara_%281960%E2%80%931975%29.png/{tamanho}px-Bandeira_do_Estado_da_Guanabara_%281960%E2%80%931975%29.png'
    }
    
    return URL + bandeira[parse.uf(uf, extintos=True)]



def brasao(uf:str, tamanho:int=100) -> str:
    '''Gera a URL da WikiMedia para o brasão de um estado de um tamanho
    escolhido.

    Parâmetros
    ----------
    uf : str
        Sigla da Unidade Federativa.
    tamanho : int (default=100)
        Tamanho em pixels da bandeira.

    Retorna
    -------
    str
        URL da bandeira do estado no formato PNG.

    Erros
    -----
    DAB_UFError
        Caso seja inserida uma UF inválida.

    Exemplos
    --------
    Gera o link para uma imagem do brasão de Santa Catarina de 200 pixels.

    >>> favoritos.brasao(uf='SC', tamanho=200)
    'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/' ...

    '''
    
    URL = r'https://upload.wikimedia.org/wikipedia/commons/thumb/'
    
    brasao = {
        'BR': f'b/bf/Coat_of_arms_of_Brazil.svg/{tamanho}px-Coat_of_arms_of_Brazil.svg.png',
        'AC': f'5/52/Brasão_do_Acre.svg/{tamanho}px-Brasão_do_Acre.svg.png',
        'AM': f'2/2c/Bras%C3%A3o_do_Amazonas.svg/{tamanho}px-Bras%C3%A3o_do_Amazonas.svg.png',
        'AL': f'5/5c/Bras%C3%A3o_do_Estado_de_Alagoas.svg/{tamanho}px-Bras%C3%A3o_do_Estado_de_Alagoas.svg.png',
        'AP': f'6/63/Bras%C3%A3o_do_Amap%C3%A1.svg/{tamanho}px-Bras%C3%A3o_do_Amap%C3%A1.svg.png',
        'BA': f'1/12/Bras%C3%A3o_do_estado_da_Bahia.svg/{tamanho}px-Bras%C3%A3o_do_estado_da_Bahia.svg.png',
        'CE': f'f/fe/Bras%C3%A3o_do_Cear%C3%A1.svg/{tamanho}px-Bras%C3%A3o_do_Cear%C3%A1.svg.png',
        'DF': f'e/e0/Bras%C3%A3o_do_Distrito_Federal_%28Brasil%29.svg/{tamanho}px-Bras%C3%A3o_do_Distrito_Federal_%28Brasil%29.svg.png',
        'ES': f'a/a0/Bras%C3%A3o_do_Esp%C3%ADrito_Santo.svg/{tamanho}px-Bras%C3%A3o_do_Esp%C3%ADrito_Santo.svg.png',
        'GO': f'b/bf/Bras%C3%A3o_de_Goi%C3%A1s.svg/{tamanho}px-Bras%C3%A3o_de_Goi%C3%A1s.svg.png',
        'MA': f'a/ab/Brasão_do_Maranhão.svg/{tamanho}px-Brasão_do_Maranhão.svg.png',
        'MG': f'd/d2/Brasão_de_Minas_Gerais.svg/{tamanho}px-Brasão_de_Minas_Gerais.svg.png',
        'MT': f'0/04/Brasão_de_Mato_Grosso.png/{tamanho}px-Brasão_de_Mato_Grosso.png',
        'MS': f'f/fa/Brasão_de_Mato_Grosso_do_Sul.svg/{tamanho}px-Brasão_de_Mato_Grosso_do_Sul.svg.png',
        'PA': f'b/bc/Brasão_do_Pará.svg/{tamanho}px-Brasão_do_Pará.svg.png',
        'PB': f'f/fd/Brasão_da_Paraíba.svg/{tamanho}px-Brasão_da_Paraíba.svg.png',
        'PE': f'0/04/Brasão_do_estado_de_Pernambuco.svg/{tamanho}px-Brasão_do_estado_de_Pernambuco.svg.png',
        'PI': f'a/ad/Brasão_do_Piauí.svg/{tamanho}px-Brasão_do_Piauí.svg.png',
        'PR': f'4/49/Brasão_do_Paraná.svg/{tamanho}px-Brasão_do_Paraná.svg.png',
        'RJ': f'5/5b/Brasão_do_estado_do_Rio_de_Janeiro.svg/{tamanho}px-Brasão_do_estado_do_Rio_de_Janeiro.svg.png',
        'RO': f'f/f1/Brasão_de_Rondônia.svg/{tamanho}px-Brasão_de_Rondônia.svg.png',
        'RN': f'2/26/Brasão_do_Rio_Grande_do_Norte.svg/{tamanho}px-Brasão_do_Rio_Grande_do_Norte.svg.png',        
        'RR': f'e/ed/Brasão_de_Roraima.svg/{tamanho}px-Brasão_de_Roraima.svg.png',
        'RS': f'3/38/Brasão_do_Rio_Grande_do_Sul.svg/{tamanho}px-Brasão_do_Rio_Grande_do_Sul.svg.png',
        'SC': f'6/65/Brasão_de_Santa_Catarina.svg/{tamanho}px-Brasão_de_Santa_Catarina.svg.png',
        'SE': f'5/52/Brasão_de_Sergipe.svg/{tamanho}px-Brasão_de_Sergipe.svg.png',
        'SP': f'1/1a/Brasão_do_estado_de_São_Paulo.svg/{tamanho}px-Brasão_do_estado_de_São_Paulo.svg.png',
        'TO': f'c/cc/Brasão_do_Tocantins.svg/{tamanho}px-Brasão_do_Tocantins.svg.png',

        # Extintos
        'FN': f'5/5a/Fernando_de_Noronha%2C_PE_-_Bras%C3%A3o.svg/{tamanho}px-Fernando_de_Noronha%2C_PE_-_Bras%C3%A3o.svg.png',
        'GB': f'c/cf/Bras%C3%A3o_do_Estado_da_Guanabara_%281960%E2%80%931975%29.png/{tamanho}px-Bras%C3%A3o_do_Estado_da_Guanabara_%281960%E2%80%931975%29.png'
    }
    
    return URL + brasao[parse.uf(uf, extintos=True)]



# Principais séries temporais do Banco Central

def ipca(**kwargs) -> _pd.DataFrame:
    return bacen.serie(433, **kwargs)

def selic(**kwargs) -> _pd.DataFrame:
    return bacen.serie(432, **kwargs)

def taxa_referencial(**kwargs) -> _pd.DataFrame:
    return bacen.serie(226, **kwargs)

def rentabilidade_poupanca(**kwargs) -> _pd.DataFrame:
    return bacen.serie(195, **kwargs)

def reservas_internacionais(periodo='mensal', **kwargs) -> _pd.DataFrame:
    if periodo.lower() == 'mensal':
        return bacen.serie(3546, **kwargs)
    elif periodo.lower() in ['diaria', 'diario', 'diário', 'diária']:
        return bacen.serie(13621, **kwargs)
    else:
        raise ValueError(
            "Período inválido. Escolha um dos seguintes valores: 'mensal' ou 'diaria'."
        )



# Principais séries temporais do Ipeadata

def risco_brasil(index=False) -> _pd.DataFrame:
    return ipea.serie(cod='JPM366_EMBI366', index=index)

def salario_minimo(tipo='nominal', index=False) -> _pd.DataFrame:
    if tipo.lower() == 'nominal':
        return ipea.serie(cod='MTE12_SALMIN12', index=index)
    elif tipo.lower() == 'real':
        return ipea.serie(cod='GAC12_SALMINRE12', index=index)
    elif tipo.lower() == 'ppc':
        return ipea.serie(cod='GAC12_SALMINDOL12', index=index)
    else:
        raise ValueError(
            "Tipo inválido. Escolha um dos seguintes valores: 'nominal', 'real' ou 'ppc'."
        )