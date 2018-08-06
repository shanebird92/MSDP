import unittest
import sys
sys.path.append('../src/msdp/')
from script import sqlquery

class TestSqlquery(unittest.TestCase):
    __skips = []
    def setUp(self):
        #print("do something before test.Prepare environment.")
        self.__my = sqlquery.Sqlquery()
        self.__months = {'1':'January',
                         '2':'February',
                         '3':'March',
                         '4':'April',
                         '5':'May',
                         '6':'June'}
        self.__debug = False

    def tearDown(self):
        #print("do something after test.Clean up.")
        pass

    def test_001(self):
        '''
            verify get_tripids_by_line()
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
            verify get_tripids_by_line()
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
	    verify get_lines_by_month('4')
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
            verify get_available_days_by_tripid()
        '''
        array = self.__my.get_available_days_by_tripid('5012600')
        self.assertTrue(len(array)>0,
                        "FAIL: Checking available days from tripid 5012600")
        self.__debug and print("Checking available days by tripids")

    @unittest.skipIf(5 in __skips,
                     "test_005 needs more than 2 minutes to run")
    def test_005(self):
        '''
            verify get_available_days_by_month()
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
            verify get_available_days_by_tripid_and_month()
        '''
        tripid = '5012600'
        months = ['6']
        for month in months:
            array = self.__my.get_available_days_by_tripid_and_month(tripid,
                                                                     month)
            self.assertTrue(len(array)>0,
                            "FAIL: Checking available days "
                            "of {} on {}".format(tripid,
                                                 self.__months[month]))
        self.__debug and print("Checking available days of {} "
                               "from {} to {}".format(tripid,
                                                      self.__months[months[0]],
                                                      self.__months[months[-1]]))

    def test_007(self):
        '''
            verify get_available_days_by_line_and_month()
        '''
        lineid = '39A'
        months = ['6']
        for month in months:
            array = self.__my.get_available_days_by_line_and_month(lineid,
                                                                   month)
            self.assertTrue(len(array)>0,
                            "FAIL: Checking available days "
                            "of {} on {}".format(lineid,
                                                 self.__months[month]))
        self.__debug and print("Checking available days of {} from "
                               "{} to {}".format(lineid,
                                                 self.__months[months[0]],
                                                 self.__months[months[-1]]))

    def test_008(self):
        '''
            verify get_arrivaltime_from_tripid_and_date(5012600, '2017-06-02')
        '''
        tripid = '5012600'
        date = '2017-06-02'
        array = self.__my.get_arrivaltime_from_tripid_and_date(tripid,
                                                               date)
        self.assertTrue(len(array)>0,
                        "FAIL: Checking arrival time list of "
                        "{} on {}".format(tripid, date))
        self.__debug and print("Checking arrival time list of "
                               "{} on {}".format(tripid,
                                                 date))

    def test_009(self):
        '''
            verify get_stoppointid_by_line('39A', 1)
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
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSqlquery)
    #suite = unittest.TestSuite()
    #suite.addTest(TestSqlquery("test_001"))
    unittest.TextTestRunner(verbosity=2).run(suite)
