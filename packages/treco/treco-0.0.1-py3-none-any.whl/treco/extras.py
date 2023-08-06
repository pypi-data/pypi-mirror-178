# TODO
# 1. Callendar
# 2. Heatmap
# 3. News

from treco.core import HEADERS, MAIN_URL, get_data_from_tables
from treco.core import get_data_from_stream

'''
Module description
-------------------
All the extra functions. 
'''


def news(amount=10, country="NULL", category="NULL"):
    '''
    Get the last news published on the Trading Economics stream.
    It is a get_data_from_stream() wrapper as for now. 

    :param amount: number of news to retrieve. 
    :param country: the name of the country (like 'France', or economic area, like 'G20' or 'euro-area'), which the news concern.
    :param category: category of news


    :return: result_json: list of dictionaries constructed on the basis of JSON response. 

    '''
    return get_data_from_stream(size=amount, country=country, category=category)


def heatmap(region=""):
    '''
    Get the heatmap, avalialbe under '/matrix' subpage. 


    :param region: economic area for which the heatmap indicators are displayed.

    :return: heatmap, Pandas dfs format.

    '''

    get_args = "?g=" + region.lower()
    url = MAIN_URL + "matrix" + get_args
    ret_val = get_data_from_tables(url)
    return ret_val


def _experimental_calendar():
    '''

    '''

    url = MAIN_URL + "calendar"
    ret_val = get_data_from_tables(url)
    return ret_val
