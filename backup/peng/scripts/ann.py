import pickle
import csv
import pandas as pd
import numpy as np

def prediction(line, startID, endID):
    model_file_a = "{}_a_2017_06.clf".format(line)
    model_file_b = "{}_b_2017_06.clf".format(line)

    time_table_file_a = "{}_a_timeTable.csv".format(line) 
    time_table_file_b = "{}_b_timeTable.csv".format(line) 

    df_a = pd.read_csv(time_table_file_a, index_col=0)
    df_b = pd.read_csv(time_table_file_b, index_col=0)

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
        sequence_a = stops_a.index(endID) - stops_a.index(startID)
    if startID in stops_b and endID in stops_b:
        sequence_b = stops_b.index(endID) - stops_b.index(startID)

    if sequence_a > sequence_b:
        pairs = sequence_a
        model_file = model_file_a
        station_number = len(stops_a)
        inputFeatures = inputFeatures_a
    elif sequence_b > sequence_a:
        pairs = sequence_b
        model_file = model_file_b
        station_number = len(stops_b)
        inputFeatures = inputFeatures_b
    else:
        return 0

    pkl_file = open(model_file, 'rb')
    new_clf = pickle.load(pkl_file)
    predictions = new_clf.predict([inputFeatures])
    
    pair_time = (predictions[0][1]-predictions[0][0])/(station_number-1)
    #print(pair_time, pairs)
    return pair_time * pairs

def main():
    print(prediction('39A', 1913, 1660))
    print(prediction('39A', 1864, 335))

if __name__ == '__main__':
    main()
