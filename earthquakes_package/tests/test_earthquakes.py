import unittest
import os
from earthquakes_package import earthquakes as e


class TestCSVReader(unittest.TestCase):

    def setUp(self):
        self.temporary_file = '/tmp/temporary_file.csv'
        f = open(self.temporary_file, 'w')
        f.close()

    def test_no_datafile(self):
        alert_info = e.get_alert_info('green', file_path="/tmp/random_name.csv")
        self.assertFalse(alert_info)

    def tearDown(self):
        os.remove(self.temporary_file)

if __name__ == '__main__':
    unittest.main()