import unittest
import sys
from datetime import timedelta, datetime

sys.path.append('../src/msdp/')
from script import weather

class TestWeather(unittest.TestCase):
    def setUp(self):
        yesterday = datetime.today() + timedelta(-1)
        y_date = str(yesterday.month).zfill(2) + '/' + \
                     str(yesterday.day).zfill(2) + '/' + \
                         str(yesterday.year)

        today = datetime.today()
        tod_date = str(today.month).zfill(2) + '/' + \
                       str(today.day).zfill(2) + '/' + \
                           str(today.year)

        tomorrow = datetime.today() + timedelta(+1)
        tom_date = str(tomorrow.month).zfill(2) + '/' + \
                       str(tomorrow.day).zfill(2) + '/' + \
                           str(tomorrow.year)

        weeks_later = datetime.today() + timedelta(+7)
        w_date = str(weeks_later.month).zfill(2) + '/' + \
                     str(weeks_later.day).zfill(2) + '/' + \
                         str(weeks_later.year)

        self.test_list = {-1:y_date,
                           0:tod_date,
                           1:tom_date,
                           7:w_date}
        self.__debug = False

    def tearDown(self):
        pass

    def test_001(self):
        '''
            test_001 assertion: verify get_difference() with input date
            expect the return value is the exact integer, comparing with the
            current day
            Scenario:
                1. Input the date of yesterday, today, tomorrow and 1 week later  
                2. Verify the returned values are -1, 0, 1, 7
        '''
        for day, test_date in self.test_list.items():
            result = weather.Weather.get_difference(test_date)      
            self.assertTrue(result == day,
                            "FAIL: Checking day's difference "
                            "from __get_difference() on day {}".format(day))
        self.__debug and print("Verify get_difference() returns valid day's difference")

    def test_002(self):
        '''
            test_002 assertion: Verify get_weather_info() does work well
            Scenario:
		1. Input the date of yesterday, today, tomorrow and 1 week later
                2. Verify the return list has 2 elements, where both of them are
                   either 0 or 1
        '''
        my = weather.Weather()
        for day, test_date in self.test_list.items():
            result = my.get_weather_info(test_date)
            self.assertTrue(len(result) == 2, "FAIL: Check returning 2 weather values from "
                                "get_weather_info() on day {}".format(day))
            self.assertTrue(result[0] == 0 or result[0] == 1,
                            "FAIL: Check returning rain value from get_weather_info() "
                            "on day {} is a valid integer (0 or 1)".format(day))
            self.assertTrue(result[1] == 0 or result[1] == 1,
                            "FAIL: Check returning sun value from get_weather_info() "
                            "on day {} is a valid integer (0 or 1)".format(day))
        self.__debug and print("Verify get_weather_info() returns valid values on Rain and Sun")


if __name__ == '__main__':
    # Select all test cases into testplate
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWeather)

    # Select particular single test case into testplate
    #suite = unittest.TestSuite()
    #suite.addTest(TestWeather("test_001"))

    # Start to run tests
    unittest.TextTestRunner(verbosity=2).run(suite)
