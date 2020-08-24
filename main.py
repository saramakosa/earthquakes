from earthquakes_package import earthquakes
import argparse



def parse_arguments():
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
    parser.add_argument("--version", action="version", version="1.0")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
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
