import requests
import datetime
import json

base_url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'
query_url = 'starttime={}&format=geojson&limit=20000&'
USGS_URL = base_url + query_url


def get_earthquake(days_past, alertlevel):
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
    r = requests.get(URL)
    events = json.loads(requests.get(URL).text)
    magnitude = 0
    place = ''
    # find the earthquake with the highest magnitude among the received results
    if len(events['features']) == 0:
        return False
    else:
        for event in events['features']:
            try:
                mag = float(event['properties']['mag'])
            except TypeError:
                pass
            if mag > magnitude:
                magnitude = mag
                place = event['properties']['place']
                
        return magnitude, place
