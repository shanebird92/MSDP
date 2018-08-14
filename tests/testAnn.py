import unittest
import sys
sys.path.append('../src/msdp/')
from script import ann

class TestAnn(unittest.TestCase):
    def setUp(self):
        self.__debug = False

    def tearDown(self):
        pass

    def test_001(self):
        '''
            test_001 assertion: input valid start&stop IDs, clocktime, rain, sun
            to expect the return values from ann.py
	    Scenario:
		1. input startPoint=328, stopPoint=7162, targetTime=72000, rain=0
                   and sun=1
                2. Verify '39A' is found as a route line
        '''
        my = ann.Ann(328,7162,72000, 0,1)
        result_list = my.get_all_prediction()      
        self.assertTrue(len(result_list) > 1, "FAIL: Checking multiple Lines are found out")
        for result in result_list:
            if result['line'] == '39A':
                self.assertTrue(result['line'] == '39A', "Checking '39A' is found out")
                break
        else:
                self.assertTrue(result['line'] == '39A', "Checking '39A' is found out")
        self.__debug and print("Checking multiple Lines are found out")

    def test_002(self):
        '''
            test_002 assertion: input reserved start&stop IDs and other valid values
            to expect returning travelTime with -1 from ann.py
            Scenario:
                1. input startPoint=7047, stopPoint=1445, targetTime=36000, rain=0 and sun=1
                2. Verify travelTime is -1,which represents that this is a reserved line of 39A
        '''
        my = ann.Ann(7047, 1445, 36000,0,1)
        result_list = my.get_all_prediction()
        for result in result_list:
            if result['line'] == '39A':
                self.assertTrue(result['travelTime'] == -1, "FAIL: Checking '39A' with reserved "
                                "start and stop IDs in bus route list")
                break
        result1 = my.new_prediction('39A')
        result2 = my.new_prediction('39A',0)
        result3 = my.new_prediction('39A',1)
        self.assertTrue(result1['travelTime'] == -1, "FAIL: Checking '39A' with reserved "
                                "start and stop IDs by default")
        self.assertTrue(result2['travelTime'] == -1, "FAIL: Checking '39A' with reserved "
                                "start and stop IDs in correct direction")
        self.assertTrue(result3['travelTime'] == 0, "FAIL: Checking '39A' with reserved "
                                "start and stop IDs in incorrect direction")
        self.__debug and print("Checking '39A' with reserved start & stop IDs")

    def test_003(self):
        '''
            test_003 assertion: Verify all keys are in returning dictionary
            Scenario:
		1. input startPoint=1913, endStops = 1660, targetTime=36900, rain=1 and sun=0
                2. Verify return dictionary include the following keys:
			- startTime
			- line
			- pairArrTime
			- pairStops
			- locations
			- isFileExist
        '''
        my = ann.Ann(1913,1660,36900,1,0)
        check_list = ['startTime',
                      'travelTime',
                      'line',
                      'pairArrTime',
                      'pairStops',
                      'locations', 'isFileExist']
        results = my.get_all_prediction()
        for result in results:
            for key in check_list:
                self.assertTrue(key in result.keys(), \
                    "FAIL: get_all_prediction() missing key "
                    "from returning dictionary: {}".format(key))

        all_results = {}
        # sub_1
        all_results['prediction()'] = my.prediction('39A')
        # sub_2
        all_results['new_prediction()_diction_0'] = my.new_prediction('39A', '0')
        # sub_3
        all_results['new_prediction()_diction_1'] = my.new_prediction('39A', '1')
        for testid, result in all_results.items():
            for key in check_list:
                self.assertTrue(key in result.keys(),
                                "FAIL: {} missing key from "
                                "returning dict: {}".format(testid, key))

        self.__debug and print("Checking all keys are in returning dictionary")

    def test_004(self):
        '''
            test_004 assertion: input invalid target clock time and other valid values
            to expect returning startTime with -1 from ann.py
            Scenario:
		1. input targetTime with -10 and 86500
                2. Verify returned 'startTime' = -1, which represents the targetTime is out
                   range of a day (0 - 86400)
	'''
        for t in [-10,86500]:
            my = ann.Ann(7047, 1445,t,0,1)
            result = my.new_prediction('39A')
            self.assertTrue(result['startTime'] == -1,
                            "FAIL: Checking start Time with invalid "
                            "inputting target clock time ({}) in bus route list".format(t))
        self.__debug and print("Checking '39A' setting up Time with "
                               "invalid inputting target clock time")

    def test_005(self):
        '''
            test_005 assertion: input valid target clock time but not suitable for planned time
            table for particular bus Line to expect returning startTime with -2 from ann.py
            Scenario:
                1. input startPoint=769, endPoint=776, targetTime=36000, rain=0 and sun=1
		2. Check line 145,116 and 7B have returned 'travelTime' = -2, which represent that
                   they don't have available travel time table
	'''
        t = 36000
        my = ann.Ann(769, 776,t,0,1)
        for line in ['145','116','7B']:
            result = my.new_prediction(line)
            self.assertTrue(result['travelTime'] == -2,
                            "FAIL: Checking travel Time with non-suitable planned Time Table "
                            "inputting target clock time ({}) in bus route {} list".format(t, line))
        self.__debug and print("Checking bus lines setting up Time with non-suitable"
                               " inputting target clock time")
        

if __name__ == '__main__':
    # Select whole test cases into test plate
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAnn)

    # Select particular single test case into test plate
    #suite = unittest.TestSuite()
    #suite.addTest(TestAnn("test_003"))

    # Start to run test cases
    unittest.TextTestRunner(verbosity=2).run(suite)
