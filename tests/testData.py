import os, sys
import json
sys.path.append('../src/msdp/')
from script import ann




def verify_one_line(busLine, stops):
    '''
        Verify one bus line from start stop to the end stop in order to
        make sure there's no error occured between each 2 stations
    '''
    singleLine = busLine.split('_')[0]
    falseCases = []
    for i in range(1,len(stops)-1):
        start = int(stops[i])
        end = int(stops[i+1])
        my = ann.Ann(start, end,36000,0,1)
        result_list = my.get_all_prediction()
        isAvailable = False
        for result in result_list:
            if result['line'] == singleLine and result['travelTime'] > 0:
                isAvailable = True
                break
        if not isAvailable:
            falseCases.append([(start, end), result_list])
    return falseCases


def main():
    data_path = os.path.dirname(os.path.abspath(__file__)) + "/test_data/"
    file = data_path + "data.json"

    with open(file) as f:
        data = json.load(f)

    startCase = '84X_a'
    isStarted = False
    for key,value in sorted(data.items()):
        if not isStarted:
            if startCase in key:
                isStarted = True
            continue
        result = verify_one_line(key, value)
        if len(result) > 0:
            print(key, "---" "FAIL")
            print("\t", result)
        else:
            print(key, "---", "PASS")

def singleTest():
    data_path = os.path.dirname(os.path.abspath(__file__)) + "/test_data/"
    file = data_path + "data.json"

    with open(file) as f:
        data = json.load(f)
    print(sorted(data.keys()))
    key = '84X_a'
    value = data[key]
    print(verify_one_line(key, value))


if __name__ == '__main__':
    main()
    #singleTest()
    
    
    
