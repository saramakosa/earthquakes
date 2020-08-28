# Earthquakes data fetching library 

This library queries the [USGS](https://earthquake.usgs.gov/fdsnws/event/1/) website to fetch the list of earthquakes registered in the last ```days``` according to their PAGER alert level (green, yellow, orange, red). The earthquake with the largest magnitude will be returned.

You can run the file named ```main.py``` id the main folder to see an example of how it works.  
After cloning the main repository, go to the downloaded folder to run the program. You can execute the main file with: ```python main.py [days] [-alertlevel] -username [username] -password [password]```.  
You can see an example below:

```
$ python main.py 10 -alertlevel green -username saramakosa -password notreal
The largest earthquake of last 10 days had magnitude 6.9 and was located at 220 km SSE of Katabu, Indonesia.
```
> **Note:** The program uses argparse, requests, datetime, json, csv, pandas, sqlite3, os, random, hashlib, and unittest.

You can also increase the verbosity of the program with the optional paramater **-v** (see sections below). You will have messages of what is happening step by step:
```
$ python main.py 10 -alertlevel green -username saramakosa -password notreal -v
Checking user credentials ...
The green level is described as having 0 estimated fatalities and < $1 million estimated losses in USD
I am now starting to search for earthquakes with the following parameters: 
days_past = 10
alertlevel = green
Search completed
The largest earthquake of last 10 days had magnitude 6.9 and was located at 220 km SSE of Katabu, Indonesia
```

**Authentication is required when runnnig the main file.**

You can find more about the PAGER (**P**rompt **A**ssessment of **G**lobal **E**arthquakes for **R**esponse) Scientific Background [here](https://earthquake.usgs.gov/data/pager/background.php). For now you just need to know how arthquakes are classified:

Alert and Color | Estimated fatalities | Estimated losses (USD)
------------ | -------------  | -------------
red | 1,000+ | $1 billion+
orange | 100 - 999 | $100 million - $1 billion
yellow | 1 - 99 |$1 million - $100 million
green |0 | < $1 million
 
> **Note:** This classification is not likely to change in the future. However, if that happens, you can modify data in ```earthquakes_package/pager_levels.csv```.  



## Usage
#### Positional arguments
- **days**: The number of days in the past as a starting point for the API call. For example, **days:2** means that you want to search for all the earthquakes in the last 48 hours.  

#### Optional arguments
- **-h, --help:** show this help message and exit 
- **-alertlevel {red, orange, yellow, green}:** PAGER fatality and economic loss impact estimates (see CSV file or table above)
- **-v:** increase the verbosity of the program
- **-username USERNAME [required]:** username
- **-password PASSWORD [required]:** password
- **--version:** show program's version number and exit.

## Database
I did not upload the ```database.db``` file containing data with users. However, there is a helper module called  ```dbmanager.py``` that will allow you to add or remove users accordingly. You can find this file in  ```/stock_package/scripts/```.  The command must be run from the parent directory as below:



#### To add a new user
From the parent directory: 
 ```
$ python earthquakes_package/scripts/dbmanager.py -a -username example -password notreal
```
Using the optional parameter **-show** you can see all the records in the users table: 

 ```
$ python earthquakes_package/scripts/dbmanager.py -a -username example -password notreal -show
Retrieving all existing users...
username: example 	password: a320823aa0c7c3ce70739429d2b15ca2ae0a9e6efed93217981e857c838a0c7e
```
> **Note:** The user's password is salted + hashed. There is no way to see its original password in plain text. If you do not remember it you can update a user's password by adding a new user with the same username.

#### To remove a user
From the parent directory: 
 ```
$ python earthquakes_package/scripts/dbmanager.py -r -username example -show
No users found!
```

## Tests
There is a test file for the functions in the earthquakes.py module. You can find them in ```/earthquakes_package/tests/``` .  
You can run the tests from the main folder with the following command:```python -m unittest -v -b earthquakes_package/tests/test_earthquakes.py ```:

```
$ python -m unittest -v -b earthquakes_package/tests/test_earthquakes.p

test_alert_info (earthquakes_package.tests.test_earthquakes.TestCSVReader)
Test that info about a correct alert level is retrieved. ... ok
test_empty_file (earthquakes_package.tests.test_earthquakes.TestCSVReader)
Test for empty file. ... ok
test_no_alert (earthquakes_package.tests.test_earthquakes.TestCSVReader)
Test for incorrect color level. ... ok
test_no_datafile (earthquakes_package.tests.test_earthquakes.TestCSVReader)
Test for non existing file. ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.003s

OK

```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## Authors
This project has been developed by [Sara Makosa](https://www.linkedin.com/in/sara-makosa-761301194/). 

## License
[MIT](https://choosealicense.com/licenses/mit/)