'''
Module description 
-------------------
Functions for getting current macro-economic indicators.
'''

from treco.core import get_data_from_tables, MAIN_URL


def indicators_by_region(region):
    '''
    List all macro-economic indicators related to given country/region/area.

    :param region: geographical region name.

    :return: indicator_lists, list of dataframes with scraped indicators.
    '''

    url = MAIN_URL + "/" + region.replace(" ", "-") + "/indicators"
    indicator_lists = get_data_from_tables(url)
    return indicator_lists


def regions_via_indicator(indicator: str, scope="World"):
    '''
    Returns a comparison of all regions/countries by one selected indicator. 

    :param indicator: name of the indicator to search for.
    :param scope: geographical cluster of countries.

    :return: region_comparison_by_one_indicator
    '''

    url = (
        MAIN_URL
        + "/country-list/"
        + indicator.lower().replace(" ", "-")
        + "?continent="
        + scope
    )

    region_comparison_by_one_indicator = get_data_from_tables(url)
    return region_comparison_by_one_indicator
