import unittest
import os
from earthquakes_package import earthquakes as e

path_to_csv = 'earthquakes_package/pager_levels.csv'

class TestCSVReader(unittest.TestCase):

    def setUp(self):
        self.temporary_file = '/tmp/temporary_file.csv'
        f = open(self.temporary_file, 'w')
        f.close()

    def test_no_datafile(self):
        """Test for non existing file."""
        alert_info = e.get_alert_info('green', file_path="/tmp/random_name.csv")
        self.assertFalse(alert_info)

        
    def test_empty_file(self):
        """Test for empty file."""
        alert_info = e.get_alert_info('random_color_that_nobody_knows',
                                      file_path=path_to_csv)
        self.assertFalse(alert_info)

    def tearDown(self):
        os.remove(self.temporary_file)

if __name__ == '__main__':
    unittest.main()