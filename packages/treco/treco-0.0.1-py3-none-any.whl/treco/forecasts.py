'''
Functions for getting forecast on:

1. Macro-economic indicators
2. Real asset related quantities.  

'''


from treco.core import MAIN_URL, get_data_from_tables, scrape_specific_tables


def forecasts_by_country(region):
    '''
    Forecast for all macro-economic indicators related to given country/region/area.

    :param region: geographical region name.

    '''
    url = MAIN_URL + "/" + region.replace(" ", "-") + "/forecasts"
    forecast_lists = get_data_from_tables(url)
    return forecast_lists


def countries_by_forecast(indicator: str, scope="World"):
    '''
    Returns a forecast of one selected indicator for multiple all the regions in given scope.

    :param indicator: name of the indicator to search for.
    :param scope: geographical cluster of countries.

    :return: region forecast by one indicator.
    '''

    url = (
        MAIN_URL
        + "/forecast/"
        + indicator.lower().replace(" ", "-")
        + "?continent="
        + scope
    )
    region_forecast_by_one_indicator = get_data_from_tables(url)
    return region_forecast_by_one_indicator


def currencies_forecast(fmt):
    ''' 
    Returns forecast of FX currency prices, as a list-of-tables. 
    Each entry in the list correspond to different geographic region.      

    :param fmt: desired output dataframe format

    :return: dataframe with currency pair ratios forecast
    '''

    ret_val = scrape_specific_tables("/forecast/currency", fmt)
    return ret_val


def stock_indices_forecast(fmt):
    '''
    Provides forecast for stock market indexes quotes for several countries including the latest price, yesterday 
    session close, plus weekly, monthly and yearly percentage changes.

    :param fmt: desired output dataframe format

    :return: dataframe with stock indices forecast
    '''
    ret_val = scrape_specific_tables("/forecast/stock-market", fmt)
    return ret_val


def commodities_forecast(fmt):
    '''
    Provides forecast for the comodity prices.

    :param fmt: desired output dataframe format

    :return: dataframe with major comodity prices forecast
    '''
    ret_val = scrape_specific_tables("/forecast/commodity", fmt)
    return ret_val


def bonds_forecast(fmt, show_all=True):
    '''
    Provides forecast for the bond prices.

    :param fmt: desired output dataframe format

    :return: dataframe with bonds data forecast
    '''

    if show_all == True:
        ret_val = scrape_specific_tables("/forecast/government-bond-10y", fmt)
        return ret_val


def crypto_forecast(fmt):
    '''
    Provides crypto forecast.

    :param fmt: desired output dataframe format

    :return: dataframe with cryptocurrency data forecast
    '''

    ret_val = scrape_specific_tables("/forecast/crypto", fmt)
    return ret_val
