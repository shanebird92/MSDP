import sys, os
sys.path.append('../src/msdp/')
from script import ann
import csv
import pandas as pd
import random


debug = False
caseNumber = 300 
line = '70'

reports = []
for direction in ['a','b']:
    data_path = os.path.dirname(os.path.abspath(__file__)) + "/test_data/"
    sample_df = pd.read_csv("{}/{}_{}_WEATHER_JUN.csv".format(data_path,line,direction),index_col=0)
    timeTable = pd.read_csv("{}/{}_{}_timeTable.csv".format(data_path,line,direction),index_col=0)
    df = sample_df.copy()
    sub_report = []
    # test method 1
    for i in range(caseNumber):
        # Get the index list from df
        index = df.index
        # Randomly select on trip
        test_index = random.randint(5,len(index))
        testCase = df.loc[test_index]

        # get column list
        columns = df.columns.values
        # get the range of stations
        rangeNum = int((len(columns)-2)/2)

        # Randomly select start and stop stations
        start_station = random.randint(1,rangeNum-5)
        stop_station = random.randint(start_station+1, rangeNum)
        stations = stop_station - start_station
        planned_time_start_station_id = "{}_P".format(str(start_station).zfill(3))
        planned_time_stop_station_id = "{}_P".format(str(stop_station).zfill(3))
        actual_time_start_station_id = "{}_A".format(str(start_station).zfill(3))
        actual_time_stop_station_id = "{}_A".format(str(stop_station).zfill(3))


        start_station = int(timeTable[planned_time_start_station_id].loc[0])
        stop_station = int(timeTable[planned_time_stop_station_id].loc[0])

        actual_travel_time = testCase[actual_time_stop_station_id] - testCase[actual_time_start_station_id]
        planned_travel_time = testCase[planned_time_stop_station_id] - testCase[planned_time_start_station_id]

        targetTime = testCase[planned_time_start_station_id]
        #print('target Time:', int(targetTime))

        rain = testCase['Rain']
        sun = testCase['Sun']
        my = ann.Ann(start_station, stop_station, targetTime,rain,sun)
        result = my.prediction(line)
        pred_travel_time = int(result['travelTime'])
        if debug:
            print("{} -> {}".format(start_station, stop_station),
                  "actual_travel_time:{}".format(actual_travel_time),
                  "pred_travel_time:{}".format(pred_travel_time),
                  "planned_travel_time:{}".format(planned_travel_time),
              "stations:{}".format(stations))
        sub_report.append([pred_travel_time - actual_travel_time, stations])
    reports.append(sub_report)

# Row data report for 2 directions
unsorted_reports = {}
for i in [0,1]:
    single_report = []
    for error in reports[i]:
        single_report.append(error[0])
    if i == 0:
        unsorted_reports['a'] = single_report
    else:
        unsorted_reports['b'] = single_report

# Create 2 dictionarys with the following format:
# {progNumber: [sum of Errors, times],...}
_summarys = []
for report in reports:
    _summary = {}
    for one in report:
         if one[1] not in _summary.keys():
             _summary[one[1]] = [one[0],1]
         else:
             count = _summary[one[1]][1] + 1
             error = _summary[one[1]][0] + one[0]
             _summary[one[1]] = [error, count]
    _summarys.append(_summary)

# Calculate Errors percentage
two = []
for report in reports:
    total = len(report)
    single_accuracy = []
    d5_list = [one for one in report if abs(one[0]) <= 300]
    d3_list = [one for one in report if abs(one[0]) <= 180]
    d1_list = [one for one in report if abs(one[0]) <= 60]
    single_accuracy.append(len(d5_list)/total)
    single_accuracy.append(len(d3_list)/total)
    single_accuracy.append(len(d1_list)/total)
    two.append(single_accuracy)
print("Accuracy percentage based on 5 mins errors: {},{}".format(two[0][0], two[1][0]))
print("Accuracy percentage based on 3 mins errors: {},{}".format(two[0][1], two[1][1]))
print("Accuracy percentage based on 1 mins errors: {},{}".format(two[0][2], two[1][2]))
#print(reports)
# Calculation on average Error for each individual progNumber
sorted_reports = {} 
for summary in _summarys:
    _report = []
    for key, values in summary.items():
        _report.append([key, round(summary[key][0]/summary[key][1],2)])        
    if 'a' not in sorted_reports.keys():
        sorted_reports['a'] = _report
    else:
        sorted_reports['b'] = _report

#print("Row data report a: {}".format(unsorted_reports['a']))
#print("Row data report b: {}".format(unsorted_reports['b']))
print("sorted report a: {}".format(sorted_reports['a']))
print("sorted report b: {}".format(sorted_reports['b']))
