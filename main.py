from earthquakes_package import earthquakes
import sys

if len(sys.argv) > 1:
    days = int(sys.argv[1])
    mag, place = earthquakes.get_earthquake(days)
    print('The largest earthquake of last {} days had magnitude {} '
          'and was located at {}'.format(days, mag, place))

else:
    print("Please write number of days in the past to start searching for!")
    exit()
    

