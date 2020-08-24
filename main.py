from earthquakes_package import earthquakes
from earthquakes_package.scripts import dbmanager
import argparse

db_abs_path = 'earthquakes_package/scripts/database.db'


def parse_arguments():
    """Parse the arguments with argparse.

    :return: The arguments parsed by argparse
    :rtype: list
    """
    alert_levels = earthquakes.get_available_levels()
    parser = argparse.ArgumentParser(
            description="Get number of days from user",
            epilog="Using FDSN	Web	Service	Specifications")
    parser.add_argument("days", help='''The number of days in the past as a
                        starting point for the research''')
    # if alertlevel is not explicit the parameter will not be added to the URL
    parser.add_argument("-alertlevel", default=None, choices=alert_levels,
                        help='''PAGER fatality and economic loss impact
                        estimates''')
    parser.add_argument("-v", help="Increase the verbosity of the program",
                        action="store_true")
    parser.add_argument('-username', help="username", required=True)
    parser.add_argument('-password', help="password", required=True)
    parser.add_argument("--version", action="version", version="1.0")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    dbmanager.open_and_create(db_abs_path)
    # If the user is not allowed to perform the action (i.e. does not exist)
    if args.v:
        print('Checking user credentials ...')
    if not dbmanager.is_allowed(args.username, args.password):
        print("Invalid credentials")
        exit()

    days = int(args.days)  # string is not allowed
    if args.alertlevel and args.v:
        level_info = earthquakes.get_alert_info(args.alertlevel)
        if level_info:
            print('The {} level is described as having {} estimated '
                  'fatalities and {} estimated losses in USD'
                  .format(level_info[0], level_info[1], level_info[2]))
        else:
            print('Alert level not found!')
            exit()
    try:
        mag, place = earthquakes.get_earthquake(days, args.alertlevel, args.v)
        print('The largest earthquake of last {} days had magnitude {} '
              'and was located at {}'.format(days, mag, place))
    except TypeError:
        print('No earthquake found with the specified parameters! Please '
              'choose a larger timespan or a lower alertlevel')
