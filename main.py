from earthquakes_package import earthquakes
import argparse

alert_levels = ['green', 'yellow', 'orange', 'red']

def parse_arguments():
    parser = argparse.ArgumentParser(
            description="Get number of days from user",
            epilog="Using FDSN	Web	Service	Specifications")
    parser.add_argument("days", help='''The number of days in the past as a
                        starting point for the research''')
    # if alertlevel is not explicit the parameter will not be added to the URL
    parser.add_argument("-alertlevel", choices=alert_levels, default=None,
                        help='''PAGER fatality and economic loss 
                        impact estimates''')
    parser.add_argument("--version", action="version", version="1.0")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    days = int(args.days) # string is not allowed
    try:
        mag, place = earthquakes.get_earthquake(days, args.alertlevel)
        print('The largest earthquake of last {} days had magnitude {} '
              'and was located at {}'.format(days, mag, place))
    except:
        print('No earthquake found with the specified parameters! Please '
              'choose a larger timespan or a lower alertlevel')
        