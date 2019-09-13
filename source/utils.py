from os import system, name
import re


def clear_console():

    '''This function clears the console
    '''

    # for windows
    if name == 'nt': 
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')


def infer_type(item):

    '''This function attempts to match the item with predefined patterns to determine its type.
       Four patterns are tested: double, integer, boolean, datetime and string

    :param item: The item to be matched with the predefined patterns
    :returns: The infered type or None
    :rtype: String or None
    '''

    if(item == None):
        return None

    # Spaces at the beginning and end of the string are removed
    trimmed_item = str(item).strip()

    ## Parse double
    #match = re.search(r'^[-+]?(?:(?:\d*\.\d+)|(?:\d+\.?))(?:[Ee][+-]?\d+)?$', trimmed_item)
    # This matching pattern forces the use of a decimal point to differentiate integers from decimals
    match = re.search(r'^[-+]?(?:(?:\d*\.\d+)|(?:\d+\.))(?:[Ee][+-]?\d+)?$', trimmed_item)

    if match:
        return 'double'

    ## Parse integer
    match = re.search(r'^[-+]?[0-9]+$', trimmed_item)

    if match:
        return 'int'

    ## Parse boolean
    match = re.search(r'^(true|false)$', trimmed_item.lower())

    if match:
        return 'boolean'

    ## Parse datetime
    match = re.search(r'^((\d{2}(?:\d{2}))[-/]\d{1,2}[-/]\d{1,2})[T\s](\d{1,2}:\d{1,2}:\d{1,2})([.]\d+)$', trimmed_item.upper())

    if match:
        return 'datetime'

    ## Parse string / paragraph
    match = re.search(r'^([\w\W]\s*)+$', trimmed_item)

    if match:
        return 'string'
    
    return None     ## If None of the previous patterns were matched!