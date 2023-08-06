'''
Module description
------------------
The module contains all core utilities and functions 
of the package related to data extraction from 
tradingeconomics. 

Additional notes
----------------
The functions presented here are NOT meant to be called
by the user. 

Functions:
----------

'''


# Necessary imports
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json


# Common constants
HEADERS = {"User-Agent": "TrecoBot/1.0"}        # The request header.
# The main website URL from which we scrape the data.
MAIN_URL = "https://tradingeconomics.com/"


def __format_dataframe(dataframe: pd.DataFrame, fmt: str):
    '''Helper function to change the format of a dataframe. 
    By default, data handling is meant to be using Pandas' dataframe, but 
    if needed - some other format can be used. 

    Supported formats: 
    ------------------
    * DataFrame -  in-program data exchange
    * json      -  file handling/in-program data exchange
    * csv       -  file handling 
    * dict      -  in-program data exchange
    * html      -  file handling 
    * pickle    -  file handling
    * latex     -  file handling / string manipulation

    Parameters:
    -----------

    : param dataframe :  dataframe to-be converted.
    : param fmt       :  target format for the df to be converted, as a string. Case insensitive. 

    '''

    fmt = fmt.lower()

    if fmt == "json":
        return dataframe.to_json()
    elif fmt == "csv":
        return dataframe.to_csv()
    elif fmt == "dict":
        return dataframe.to_dict()
    elif fmt == "html":
        return dataframe.to_html()
    elif fmt == "numpy" or "np":
        return dataframe.to_numpy()
    elif fmt == "pickle":
        return dataframe.to_pickle()
    elif fmt == "latex":
        return dataframe.to_latex()
    else:
        return dataframe


def get_data_from_stream(begin=0, size=1, country="NULL", category="NULL") -> list:
    '''The function requests and receives the data directly from news stream back-end endpoint.
    It is a very simple function, manipulating the get request string.

    It's capabilities are limited by built-in safety mechanisms such as this one -  the maximum amount of news to be scraped cannot 
    exceed 100 news in a single querry. To obtain more (consecutive) news, for example 300, one would have to:

    1. Set index to 0
    2. Set the size to 100 
    3. Scrape the data from 0 to 0+100 indices, then again...
    4. Set the beginning index to 100 (hundreth scraped news)
    5. Set the size to 100 (max)
    6. Scrape the data - from 100 to 100+100  


    :param begin: initial index of the news to be scraped. The news are ordered always from the newest (index == 0) to the oldest (index == len(database))
    :param size: number of news to be scraped. (max == 100)


    :return: result_json : list of dictionaries constructed on the basis of JSON response. 



    '''

    headers = HEADERS
    stream_url = "https://tradingeconomics.com/ws/stream.ashx"

    stream_get_args = "?start={begin}&size={size}".format(
        begin=begin, size=size)
    if country != "NULL":
        stream_get_args += "c={}".format(country.lower().replace(" ", "+"))
    if country != "NULL":
        stream_get_args += "i={}".format(category.lower().replace(" ", "+"))

    url = stream_url + stream_get_args

    resp = requests.get(url, headers=headers)

    soup = BeautifulSoup(resp.content, "html.parser", from_encoding="utf-8")

    result_json = json.loads(soup.text.encode("utf-8", "ignore"))

    return result_json


def get_data_from_tables(url: str) -> list:
    '''Function allowing to obtain data from the tables presented on the website.
    The function finds all the tables in given page, downloads its contents, 
    and returns them in the form of list of dataframes (each dataframe represent different table). 


    :param url : address from which we're scraping the data


    :return: list of dataframes

    '''

    headers = HEADERS

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    tables = soup.find_all("table", "table")

    df_tables_list = []

    for table in tables:
        df_table = pd.read_html(str(table))
        df_tables_list.append(df_table[0])

    return df_tables_list


def scrape_specific_tables(server_path, fmt):
    '''
    Encapsulation of some of the utilities used by 
    the other modules, for scraping data from tables. 

    :param server_path: hard-coded part of the URL adres with presented tables
    :param fmt: format of the resulting querry
    :return: dataframe_list
    '''

    url = MAIN_URL + server_path
    dataframe_list = get_data_from_tables(url)
    for dataframe in dataframe_list:
        __format_dataframe(dataframe=dataframe, fmt=fmt)

    return dataframe_list


def get_data_from_lists(url: str, as_list=False):
    '''
    Function allowing to obtain data from the lists presented on the website.
    The function finds all the list in given page, downloads its contents, 
    and returns them. 

    :param url: address from which we're scraping the data
    :param as_list : if True the returned value is list of dictionaries. Otherwise it's a dictionary of dictionaries.

    :param df_return: dictionary of dictionaires or list of dictionaries depending on - as_list parameter
    '''

    headers = HEADERS
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    lists = soup.find_all("ul", {"class": "list-unstyled"})

    df_return = {}
    if as_list:
        df_return = []

    for list_ in lists:

        list_contents = list_.find_all("li")
        df_list_contents = {}
        key = ""

        for list_item in list_contents:
            a = list_item.find("a")
            if a is not None:
                df_list_contents[list_item.text] = a.get("href")
            else:
                key = list_item.text
        if as_list == True:
            df_return.append([key, df_list_contents])
        else:
            df_return[key] = df_list_contents

    return df_return
