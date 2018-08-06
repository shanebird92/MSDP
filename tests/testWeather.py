import unittest
import sys
from datetime import timedelta, datetime

sys.path.append('../src/msdp/')
from script import weather

class TestWeather(unittest.TestCase):
    def setUp(self):
        #print("do something before test.Prepare environment.")
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
        #print("do something after test.Clean up.")
        pass

    def test_001(self):
        '''
            test_001 assertion: verify get_difference()
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
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWeather)
    #suite = unittest.TestSuite()
    #suite.addTest(TestWeather("test_001"))
    unittest.TextTestRunner(verbosity=2).run(suite)
