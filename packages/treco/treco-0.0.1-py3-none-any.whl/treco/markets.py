"""
Set of functions allowing to get the current values of
real asset related quantities.  

The functions return lists of tables.
The data in each table is formatted in a fixed way; 
that is:

1. Name of the indicator
2. Actual value (price, ratio, quotation etc.)
3. Point-wise change daily
4. Percentage change daily
5. Percentage change weekly
6. Percentage change monthly
7. Percentage YoY 
8. Today's date.

"""


from treco.core import scrape_specific_tables


def currencies(fmt):
    ''' 
    Returns FX currency prices, as a list-of-tables. 
    Each entry in the list correspond to different geographic region.      

    :param fmt: desired output dataframe format
    :return: dataframe with currency pair ratios
    '''

    ret_val = scrape_specific_tables("/currencies", fmt)
    return ret_val


def stock_indices(fmt):
    '''
    Provides stock market indexes quotes for several countries including the latest price, yesterday 
    session close, plus weekly, monthly and yearly percentage changes.


    :param fmt: desired output dataframe format
    :return: dataframe with stock indices
    '''

    ret_val = scrape_specific_tables("/stocks", fmt)
    return ret_val


def commodities(fmt):
    '''
    Provides current commodity prices.

    :param fmt: desired output dataframe format

    :return: dataframe with major comodity prices
    '''

    ret_val = scrape_specific_tables("/commodities", fmt)
    return ret_val


def bonds(fmt):
    '''
    Provides current prices for global bond market.

    :param fmt: desired output dataframe format

    :return: dataframe with bonds data
    '''

    ret_val = scrape_specific_tables("/bonds", fmt)
    return ret_val


def crypto(fmt):
    '''
    Provides current prices for major cryptocurrencies.

    :param fmt: desired output dataframe format

    :return: dataframe with cryptocurrency data 
    '''

    ret_val = scrape_specific_tables("/crypto", fmt)
    return ret_val
