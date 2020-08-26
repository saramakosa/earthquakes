import requests
import datetime
import json
import csv
import pandas as pd


base_url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'
query_url = 'starttime={}&format=geojson&limit=20000&'
USGS_URL = base_url + query_url
path_to_csv = 'earthquakes_package/pager_levels.csv'


def get_alert_info(level, file_path=path_to_csv):
    """Get the description of an alert level given by the user

    :param level: The PAGER alert level given by the user
    :type file_path: string
    :param file_path: The path to the csv file
    :type file_path: string
    :return: The official description elements of the chosen alert level
    :rtype: list
    """
    try:
        with open(file_path) as csvfile:
            inforeader = csv.reader(csvfile, delimiter=',')
            next(inforeader)  # skip the header
            for row in inforeader:
                if row[0] == level:
                    return row
            # if the level is not found in the csv return False
            return False
    # if the file is not found (maybe incorrect name) return False
    except FileNotFoundError:
        return False


def get_available_levels(file_path=path_to_csv):
    """Return the choices available for the PAGER alert levels.

    :param file_path: The path to the csv file
    :type file_path: string
    :return: The PAGER alert levels available
    :rtype: list
    """
    df = pd.read_csv(file_path, index_col=False)
    choices = df['alert_and_color'].tolist()
    return choices


def get_earthquake(days_past, alertlevel, verbosity):
    """Return the magnitude and the place of the earthquake with the highest
    magnitude given a starting time.

    :param days_past: Number of days in the past (used as starting point)
    :type days_past: int
    :return: The magnitude and the place of the strongest earthquake found
    :rtype: float, string
    """
    # get the date of today - days_past days at 00 AM
    start_date = (datetime.datetime.now() +
                  datetime.timedelta(days=-days_past)).strftime("%Y-%m-%d")
    URL = USGS_URL.format(start_date)
    # add the parameter alertlevel only if specified by the user
    if alertlevel:
        URL = URL + '&alertlevel=' + alertlevel
    if verbosity:
        print('I am now starting to search for earthquakes with the following '
              'parameters: \ndays_past = {}\nalertlevel = {}'
              .format(days_past, alertlevel))
    r = requests.get(URL)
    events = json.loads(requests.get(URL).text)
    magnitude = 0
    place = ''
    # find the earthquake with the highest magnitude among the received results
    if verbosity:
        print('Search completed')
    if len(events['features']) == 0:
        return False, False
    # iterate all the events and find the one with the largest magnitude
    for event in events['features']:
        try:
            mag = float(event['properties']['mag'])
        except TypeError:
            pass
        if mag > magnitude:
            magnitude = mag
            place = event['properties']['place']
    return magnitude, place
