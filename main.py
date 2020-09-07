"""This module executes a call to the USGS service and returns the largest
 earthquake in the last [last_days] where last_days is chosen by the user.
The module parse_arguments provides more information about the arguments that
 can be used."""

from earthquakes_package import earthquakes
from earthquakes_package.scripts import dbmanager
import argparse

db_abs_path = 'earthquakes_package/scripts/database.db'


def parse_arguments():
    """Parse the arguments with argparse.

    :return: The arguments parsed by argparse
    :rtype: list
    """
    # get the PAGER alert level codes (from the CSV)
    alert_levels = earthquakes.get_available_levels()
    parser = argparse.ArgumentParser(
            description="Get number of days in the past to use as starttime",
            epilog="Using FDSN	Web	Service	Specifications")
    parser.add_argument("days", help='''The number of days in the past as a
                        starting point for the API call''')
    # if alertlevel is not made explicit it will not be added to the URL
    parser.add_argument("-alertlevel", default=None, choices=alert_levels,
                        help='''PAGER fatality and economic loss impact
                        estimates (see CSV file)''')
    parser.add_argument("-v", help="Increase the verbosity of the program",
                        action="store_true")
    # username and password required for any action
    parser.add_argument('-username', help="username", required=True)
    parser.add_argument('-password', help="password", required=True)
    parser.add_argument("--version", action="version", version="1.0")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    # See first if the user is allowed to perform the action
    dbmanager.open_and_create(db_abs_path)
    if args.v:
        print('Checking user credentials ...')
    if not dbmanager.is_allowed(args.username, args.password):
        print("Invalid credentials, please check username and password")
        exit()

    # IF THE USER IS ALLOWED ...
    days = int(args.days)
    # If the alert level is made explicit by the user verbosity is set to true
    # describe the alert level to the user
    if args.alertlevel and args.v:
        level_info = earthquakes.get_alert_info(args.alertlevel)
        if level_info:
            print('The {} level is described as having {} estimated '
                  'fatalities and {} estimated losses in USD'
                  .format(level_info[0], level_info[1], level_info[2]))
    # search for the earthquakes
    mag, place = earthquakes.get_earthquake(days, args.alertlevel, args.v)
    if mag and place:
        print('The largest earthquake of last {} days had magnitude {} '
              'and was located at {}'.format(days, mag, place))
    else:
        print('No earthquake found with the specified parameters! Please '
              'choose a larger timespan or a lower alertlevel')
