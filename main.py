from earthquakes_package import earthquakes
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
            description="Get number of days from user",
            epilog="Using FDSN	Web	Service	Specifications")
    parser.add_argument("days", help='''The number of days in the past as a
                        starting point for the research''')
    parser.add_argument("--version", action="version", version="1.0")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    days = int(args.days) # string is not allowed
    mag, place = earthquakes.get_earthquake(days)
    print('The largest earthquake of last {} days had magnitude {} '
          'and was located at {}'.format(days, mag, place))