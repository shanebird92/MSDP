import unittest
import sys
sys.path.append('../src/msdp/')
from script import ann

class TestAnn(unittest.TestCase):
    def setUp(self):
        self.__debug = False

    def tearDown(self):
        #print("do something after test.Clean up.")
        pass

    def test_001(self):
        '''
            test_001 assertion: input valid start&stop IDs, clocktime, rain, sun
            to expect the return values from ann.py
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
        '''
        my = ann.Ann(1913,1660,36900,1,0)
        check_list = ['startTime',
                      'travelTime',
                      'line',
                      'pairArrTime',
                      'pairStops',
                      'locations']
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

    def test_006(self):
        '''
            test_006 assertion: input invalid target clock time and other valid values
            to expect returning startTime with -1 from ann.py
	'''
        for t in [-10,86500]:
            my = ann.Ann(7047, 1445,t,0,1)
            result = my.new_prediction('39A')
            self.assertTrue(result['startTime'] == -1,
                            "FAIL: Checking start Time with invalid "
                            "inputting target clock time ({}) in bus route list".format(t))
        self.__debug and print("Checking '39A' setting up Time with "
                               "invalid inputting target clock time")

    def test_007(self):
        '''
            test_007 assertion: input valid target clock time but not suitable for planned time
            table for particular bug Line to expect returning startTime with -1 from ann.py
	'''
        t = 36000
        my = ann.Ann(769, 776,t,0,1)
        for line in ['145','116','7B']:
            result = my.new_prediction(line)
            self.assertTrue(result['travelTime'] == -1,
                            "FAIL: Checking travel Time with non-suitable planned Time Table "
                            "inputting target clock time ({}) in bus route {} list".format(t, line))
        self.__debug and print("Checking bus lines setting up Time with non-suitable"
                               " inputting target clock time")
        

if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAnn)
    #suite = unittest.TestSuite()
    #suite.addTest(TestAnn("test_007"))
    unittest.TextTestRunner(verbosity=2).run(suite)
