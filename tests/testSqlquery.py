import unittest
import sys
sys.path.append('../src/msdp/')
from script import sqlquery

class TestSqlquery(unittest.TestCase):
    __skips = []
    def setUp(self):
        self.__my = sqlquery.Sqlquery()
        self.__months = {'1':'January',
                         '2':'February',
                         '3':'March',
                         '4':'April',
                         '5':'May',
                         '6':'June'}
        self.__debug = False

    def tearDown(self):
        pass

    def test_001(self):
        '''
            test_001 assertion: Verify get_tripids_by_line() with valid input months(1-6), expect
            getting a group of tripIDs
            Scenario:
		1. input month from 1 to 6
		2. input line with '39A'
                3. Verify the query result has more than 500 tripIDs for each month
        '''
        for month in ['1','2','3','4','5','6']:
            array = self.__my.get_tripids_by_line('39A', month)
            self.assertTrue(len(array) > 500,
                            "FAIL: Checking available tripids of "
                            "route 39A in {}".format(self.__months[month]))
        self.__debug and print("Checking available tripids of route 39A "
                               "from {} to {}".format(self.__months['1'],
                                                      self.__months['6']))     

    def test_002(self):
        '''
            test_002 assertion: Verify get_lines_by_tripid() with valid input tripid, expect getting
            the exact bus line
	    Scenario:
		1. Input 2 tripds picking from Line 27 and Line 39A
                2. Verify the return values are '27' and '39A' exactly
        '''
        testdata = {'5012600': '27', '4335079':'39A'}
        for tripid, sline in testdata.items():
            line = self.__my.get_lines_by_tripid(tripid)
            self.assertTrue(line == sline,
                            "FAIL: Checking available bus "
                            "line {} from tripid {}".format(sline, tripid))
        self.__debug and print("Checking available bus lines from tripids")

    def test_003(self):
        '''
	    test_003 assertion: Verify get_lines_by_month() with valid input month, expect getting
            more than 120 lines as the query result
	    Scenario:
		1. Input months from 1 to 6 (one by one)
                2. Verify the return value is a list which has more than 120 bus lines
        '''
        for month in ['1','2','3','4','5','6']:
            array = self.__my.get_lines_by_month(month)
            self.assertTrue(len(array) > 120,
                            "FAIL: Checking available bus lines "
                            "from in {}".format(self.__months[month]))
        self.__debug and print("Checking available bus lines from "
                               "between {} to {}".format(self.__months['1'],
                                                         self.__months['6']))     

    @unittest.skipIf(4 in __skips,
                     "test_004 needs more than 5 minutes to run")
    def test_004(self):
        '''
            test_004 sertion: Verify get_available_days_by_tripid() with a valid input tripid, expect
            getting several available days (date time)
            Scenario:
                1. Select an example tripid (5012600) as input value
                2. Verify it can return more than or equal 1 available dates as a query
                   result
        '''
        array = self.__my.get_available_days_by_tripid('5012600')
        self.assertTrue(len(array)>0,
                        "FAIL: Checking available days from tripid 5012600")
        self.__debug and print("Checking available days by tripids")

    @unittest.skipIf(5 in __skips,
                     "test_005 needs more than 2 minutes to run")
    def test_005(self):
        '''
            test_005 assertion: Verify get_available_days_by_month() with a particular month, expect
            getting serveral available days
            Scenario:
                1. Input month from 1 to 6 (one by one)
		2. Verify it can return more than or equal 1 available day (date time)
                   as a query result
        '''
        for month in ['1','2','3','4','5','6']:
            array = self.__my.get_available_days_by_month(month)
            self.assertTrue(len(array)>0,
                            "FAIL: Checking available days "
                            "from {}".format(self.__months[month]))
        self.__debug and print("Checking available days "
                               "from {} to {}".format(self.__months['1'],
                                                      self.__months['6']))

    def test_006(self):
        '''
            test_006 assertion: Verify get_available_days_by_tripid_and_month() with input month and tripid,
            expect getting available days list (date time)
	    Scenario:
                1. Input a particular tripID and month (from 1 to 6)
                2. Verify it returns more than or equal 1 avaliable day (date time)
        '''
        testData = {'5002343':'1',
                    '4348986':'2',
                    '4519838':'3',
                    '4525946':'4',
                    '5013461':'5',
                    '5014001':'6'}
        for tripid, month in testData.items():
            array = self.__my.get_available_days_by_tripid_and_month(tripid,
                                                                     month)
            self.assertTrue(len(array)>=1,
                            "FAIL: Checking available days "
                            "of {} on {}".format(tripid,
                                                 self.__months[month]))
        self.__debug and print("Checking available days of {} "
                               "from {} to {}".format(tripid,
                                                      self.__months[months[0]],
                                                      self.__months[months[-1]]))

    def test_007(self):
        '''
            test_007 assertion: Verify get_available_days_by_line_and_month() with input line and month,
            expect getting available days list (date time)
            Scenario:
                1. Input a particular line and months from 1 to 6 (one by one)
                2. Verify the return value is a list which is more than 10
                   available days (date time)
        '''
        lineid = '39A'
        months = ['1','2','3','4','5', '6']
        for month in months:
            array = self.__my.get_available_days_by_line_and_month(lineid,
                                                                   month)
            self.assertTrue(len(array)>10,
                            "FAIL: Checking available days "
                            "of {} on {}".format(lineid,
                                                 self.__months[month]))
        self.__debug and print("Checking available days of {} from "
                               "{} to {}".format(lineid,
                                                 self.__months[months[0]],
                                                 self.__months[months[-1]]))

    def test_008(self):
        '''
            test_008 assertion: Verify get_arrivaltime_from_tripid_and_date() with input tripid and
            particular data time, expect getting a list of arrival time
            Scenario:
                1. Input particular tripID and a date
                2. Verify the return value is a list which is more than 50
                   arrival time
        '''
        tripid = '5012600'
        date = '2017-06-02'
        array = self.__my.get_arrivaltime_from_tripid_and_date(tripid,
                                                               date)
        self.assertTrue(len(array)>50,
                        "FAIL: Checking arrival time list of "
                        "{} on {}".format(tripid, date))
        self.__debug and print("Checking arrival time list of "
                               "{} on {}".format(tripid,
                                                 date))

    def test_009(self):
        '''
            test_009 assertion: Verify get_stoppointid_by_line() with input line, expect getting more than 
            or equal available stops
            Scenario:
                1. Input a set of lines
                2. Verify the return is a list of stopIDs
        '''
        lineids = ['46A', '39A']
        directions = [1,2]
        for lineid in lineids:
            for d in directions:
                array = self.__my.get_stoppointid_by_line(lineid, d)
                self.assertTrue(len(array)>0,
                                "FAIL: Checking available stop point IDs list of "
                                "{} on direction {}".format(lineid, d))
        self.__debug and print("Checking 2 bus lines({} and {})'s available stop "
                               "point IDs list on direction 1 and 2".format(lineids[0],
                                                                            lineids[1]))

if __name__ == '__main__':
    # Select all test cases into test plate
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSqlquery)

    # Select particular test case into test plate
    #suite = unittest.TestSuite()
    #suite.addTest(TestSqlquery("test_008"))

    # Start to run test cases
    unittest.TextTestRunner(verbosity=2).run(suite)
