import unittest
import sys
sys.path.append('../src/msdp/')
from script import ann

class TestAnn(unittest.TestCase):
    def setUp(self):
        #print("do something before test.Prepare environment.")
        pass

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
        print("Checking multiple Lines are found out")

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
        print("Checking '39A' with reserved start & stop IDs")

    def test_003(self):
        '''
            test_003 assertion: input invalid target clock time and other valid values
            to expect returning startTime with -1 from ann.py
	'''
        for t in [-10,86500]:
            my = ann.Ann(7047, 1445,t,0,1)
            result = my.new_prediction('39A')
            self.assertTrue(result['startTime'] == -1, "FAIL: Checking start Time with invalid "
                            "inputting target clock time ({}) in bus route list".format(t))
        print("Checking '39A' setting up Time with invalid inputting target clock time")
        

if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAnn)
    unittest.TextTestRunner(verbosity=2).run(suite)
