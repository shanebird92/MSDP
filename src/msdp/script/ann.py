import pickle, os
import csv, json
import pandas as pd
import numpy as np

class Ann:
    def __init__(self, startID, endID, targetTime, rain, sun, DEBUG=False):
        self.__data_path = os.path.dirname(os.path.abspath(__file__)) + "/../../../data"
        self.__startid = startID
        self.__endid = endID
        self.__targettime = targetTime
        self.__debug = DEBUG
        self.__rain = rain
        self.__sun = sun

    @staticmethod
    def get_mean_timetable(df, start_location, target_time):
        station_column = '{}_P'.format(str(start_location).zfill(3))
        mean_array = df[abs(df[station_column]-target_time) == \
            min(abs(df[station_column]-target_time))].mean()
        return mean_array.values

    def new_prediction(self, line, direction=''):
        '''
	    optimized prediction method with particular direction	
        '''
        pred_report = {}
        pred_report['line'] = line
        pred_report['travelTime'] = 0
        pred_report['startTime'] = 0
        pred_report['pairStops'] = []
        pred_report['pairArrTime'] = []

        startID = self.__startid
        endID = self.__endid
        targetTime = self.__targettime
        if len(direction) == 0:
            return self.prediction(line)
        else:
            try:
                if direction == '0':
                    model_file = self.__data_path + "/{}_a_2017_06.clf".format(line)
                    time_table_file = self.__data_path + "/{}_a_timeTable.csv".format(line) 
                elif direction == '1':
                    model_file = self.__data_path + "/{}_b_2017_06.clf".format(line)
                    time_table_file = self.__data_path + "/{}_b_timeTable.csv".format(line) 
                df = pd.read_csv(time_table_file, index_col=0)
            except Exception as e:
                if self.__debug:
                    print("Warning: Line {} {}".format(line, str(e)))
                return pred_report

            stops = []
            inputFeatures = []
            for column in df.columns:
                # Get all stopPointIDs from planned time table file
                stops.append(df[column].loc[0])
                # Get all stations' planned arrival time from planned time table file
                inputFeatures.append(df[column].iloc[1])
            stop_location = stops.index(endID)
            start_location = stops.index(startID)
            pairs = stop_location - start_location

            station_number = len(stops)
            # Getting the plannted Time Table arrary from first station to last station
            plannedTimeArray = self.get_mean_timetable(df,
                                                       start_location,
                                                       targetTime)
            
            if len(plannedTimeArray) == station_number:
                plannedTime_first = plannedTimeArray[0]
                plannedTime_end = plannedTimeArray[-1]
                plannedTime_start = plannedTimeArray[start_location]
                plannedTime_stop = plannedTimeArray[stop_location]
            else:
                print("ERROR NOTICE: Can not get mean planned "
                      "arrival time from time table!")
                plannedTime_first = df[df.columns[0]].iloc[1]
                plannedTime_end = df[df.columns[-1]].iloc[1]
                plannedTime_start = df[df.columns[start_location]].iloc[1]
                plannedTime_stop = df[df.columns[stop_location]].iloc[1]

        try:
            pkl_file = open(model_file, 'rb')
            new_clf = pickle.load(pkl_file)
        except Exception as e:
            if self.__debug:
                print("Warning: Line {} {}".format(line, str(e)))
            return pred_report
        inputFeatures.append(self.__sun)
        inputFeatures.append(self.__rain)
        predictions = new_clf.predict([inputFeatures])
    
        # get the predicted bus setup time
        pred_start_time = predictions[0][0]

        pred_full_time = predictions[0][1] - predictions[0][0]
        planned_full_time = plannedTime_end - plannedTime_first
        planned_pairs_time = plannedTime_stop - plannedTime_start
        pred_pairs_time = pred_full_time * planned_pairs_time / planned_full_time

        # Create a dict for storing all information from prediction
        pred_report['travelTime'] = pred_pairs_time
        pred_report['startTime'] = pred_start_time
        pred_report['pairStops'] = stops[start_location:(stop_location+1)]
        pred_report['pairArrTime'] = inputFeatures[start_location:(stop_location+1)]

        return pred_report

    def prediction(self, line):
        '''
	- input value:
		line: bus route, such as 39A, 46A, etc.
		startID: start station ID
                endID: end station ID
                targetTime: the o'clock time when taking bus
				from start station, it is seconds
                                to midnight
        - Return Value:
                dictionary including travelTime, startTime, paired stops and paired arrival time
        '''
        # create a dict to store predicting information
        pred_report = {}
        pred_report['line'] = line
        pred_report['travelTime'] = 0
        pred_report['startTime'] = 0
        pred_report['pairStops'] = []
        pred_report['pairArrTime'] = []

        startID = self.__startid
        endID = self.__endid
        targetTime = self.__targettime
        try:
            model_file_a = self.__data_path + "/{}_a_2017_06.clf".format(line)
            model_file_b = self.__data_path + "/{}_b_2017_06.clf".format(line)

            time_table_file_a = self.__data_path + "/{}_a_timeTable.csv".format(line) 
            time_table_file_b = self.__data_path + "/{}_b_timeTable.csv".format(line) 

            df_a = pd.read_csv(time_table_file_a, index_col=0)
            df_b = pd.read_csv(time_table_file_b, index_col=0)

        except Exception as e:
            if self.__debug:
                print("Warning: Line {} {}".format(line, str(e)))
            return 0

        stops_a = []
        inputFeatures_a = []
        for column in df_a.columns:
            stops_a.append(df_a[column].loc[0])
            inputFeatures_a.append(df_a[column].iloc[1])
        stops_b = []
        inputFeatures_b = []
        for column in df_b.columns:
            stops_b.append(df_b[column].loc[0])
            inputFeatures_b.append(df_b[column].iloc[1])

        sequence_a = 0
        sequence_b = 0
        if startID in stops_a and endID in stops_a:
            stop_location = stops_a.index(endID)
            start_location = stops_a.index(startID)
            sequence_a = stop_location - start_location
        if startID in stops_b and endID in stops_b:
            stop_location = stops_b.index(endID)
            start_location = stops_b.index(startID)
            sequence_b = stop_location - start_location


        if sequence_a > sequence_b:
            pairs = sequence_a
            model_file = model_file_a
            station_number = len(stops_a)
            inputFeatures = inputFeatures_a
            stops = stops_a
            plannedTimeArray = self.get_mean_timetable(df_a,
                                                       start_location,
                                                       targetTime)

            if len(plannedTimeArray) == station_number:
                plannedTime_first = plannedTimeArray[0]
                plannedTime_end = plannedTimeArray[-1]
                plannedTime_start = plannedTimeArray[start_location]
                plannedTime_stop = plannedTimeArray[stop_location]
            else:
                print("ERROR NOTICE: Can not get mean planned "
                      "arrival time from time table!")
                plannedTime_first = df_a[df_a.columns[0]].iloc[1]
                plannedTime_end = df_a[df_a.columns[-1]].iloc[1]
                plannedTime_start = df_a[df_a.columns[start_location]].iloc[1]
                plannedTime_stop = df_a[df_a.columns[stop_location]].iloc[1]
        elif sequence_b > sequence_a:
            pairs = sequence_b
            model_file = model_file_b
            station_number = len(stops_b)
            inputFeatures = inputFeatures_b
            stops = stops_b
            plannedTimeArray = self.get_mean_timetable(df_b,
                                                       start_location,
                                                       targetTime)

            if len(plannedTimeArray) == station_number:
                plannedTime_first = plannedTimeArray[0]
                plannedTime_end = plannedTimeArray[-1]
                plannedTime_start = plannedTimeArray[start_location]
                plannedTime_stop = plannedTimeArray[stop_location]
            else:
                print("ERROR NOTICE: Can not get mean planned "
                      "arrival time from time table!")
                plannedTime_first = df_b[df_b.columns[0]].iloc[1]
                plannedTime_end = df_b[df_b.columns[-1]].iloc[1]
                plannedTime_start = df_b[df_b.columns[start_location]].iloc[1]
                plannedTime_stop = df_b[df_b.columns[stop_location]].iloc[1]
        else:
            return pred_report

        try:
            pkl_file = open(model_file, 'rb')
            new_clf = pickle.load(pkl_file)
        except Exception as e:
            if self.__debug:
                print("Warning: Line {} {}".format(line, str(e)))
            return pred_report
        inputFeatures.append(self.__sun)
        inputFeatures.append(self.__rain)
        predictions = new_clf.predict([inputFeatures])
    
        pred_full_time = predictions[0][1] - predictions[0][0]
        planned_full_time = plannedTime_end - plannedTime_first
        planned_pairs_time = plannedTime_stop - plannedTime_start
        pred_pairs_time = pred_full_time * planned_pairs_time / planned_full_time

        pred_report['travelTime'] = pred_full_time
        pred_report['startTime'] = predictions[0][0]
        pred_report['pairStops'] = stops[start_location:(stop_location+1)]
        pred_report['pairArrTime'] = inputFeatures[start_location:(stop_location+1)]
        return pred_report

    def get_lines(self):
        '''
	    Get available Lines from privided startID and endID
        '''
        startID = self.__startid
        endID = self.__endid
        json_file = '{}/stops.json'.format(self.__data_path)
        all_lines = json.loads(open(json_file).read())
        if str(startID) in all_lines.keys():
            startID_lines = all_lines[str(startID)]
        else:
            return []
        if str(endID) in all_lines.keys():
            endID_lines = all_lines[str(endID)]
        else:
            return []
        lines = set(startID_lines)&set(endID_lines)
        new_lines = []
        for line in lines:
            new_lines.append(line.split('_'))
        return new_lines

    def get_all_prediction(self):
        lines = self.get_lines()
        if self.__debug:
            print("Searching from bus lines table: ", lines)
        results = []
        for oneLine in lines:
            results.append(self.new_prediction(oneLine[0], oneLine[1]))
        return results

def main():
    #my = Ann(1864,335,34200,0,0,DEBUG=True)
    #my = Ann(6112,1867,24200,0,0)
    '''
    my = Ann(1913,1660,72000,0,1, DEBUG=True)
    print(my.get_all_prediction())
    my = Ann(1913,1660,72000,0,0, DEBUG=True)
    print(my.get_all_prediction())
    my = Ann(1913,1660,72000,1,1, DEBUG=True)
    print(my.get_all_prediction())
    print(my.get_all_prediction())
    print(my.prediction('39'))
    '''
    #my = Ann(1913,1660,72000,1,0, DEBUG=True)
    my = Ann(328,7162,72000, 0,1, DEBUG=True)
    #my = Ann(328,1805,72000,0,1, DEBUG=True)
    #my = Ann(328,7162,72000,0,1, DEBUG=True)
    #print(my.prediction('39A'))
    print(my.get_all_prediction())

if __name__ == '__main__':
    main()
