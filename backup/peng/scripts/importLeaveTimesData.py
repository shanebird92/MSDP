# Author: Peng Ye
# Date: 19/06/2018

import MySQLdb
import sys
def dateConvert(str):
    array = str.split()
    str_array = array[0].split('-')
    months = {'JAN':'01', 'FEB':'02','MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08'}
    year = 2000 + int(str_array[2])
    month = months[str_array[1]]
    day = str_array[0]
    dateTime = "{}-{}-{}".format(year, month, day)
    return dateTime


def main(file):
    print("Warning: You are tying to import huge size of data into database! Quite now! Comment the code after this line in script first!")
    sys.exit()
    try:
        conn = MySQLdb.connect(host = "127.0.0.1",
                          user = "root",
                          passwd="MSDPUCD",
                          db = "SummerProject")
        x = conn.cursor()
    except Exception as e:
        print(str(e))
        return 1
    handle = open(file, 'r')
    line = handle.readline()
    lineArray = []
    #  ['TripId', 'DataSource', 'DayOfService', 'ProgrNumber', 'StopPointId',
    #   'PlannedTime_Arr', 'PlannedTime_Dep', 'ActualTime_Arr',
    #   'ActualTime_Dep', 'Vehicleid'
    #   ]
    row = {}
    count = 0
    while(len(line) != 0):
        #print(len(lineArray),lineArray)
        #if count == 300:
        #    break;
        try:
            line = handle.readline().strip()
            lineArray = line.split(';')
            row[0] = int(lineArray[2])
            row[1] = lineArray[0]
            row[2] = dateConvert(lineArray[1])
            row[3] = int(lineArray[3])
            row[4] = int(lineArray[4])
            if len(lineArray[5]) == 0:
                row[5] = 0
            else:
                row[5] = lineArray[5]
            if len(lineArray[6]) == 0:
                row[6] = 0
            else:
                row[6] = lineArray[6]
            if len(lineArray[7]) == 0:
                row[7] = 0
            else:
                row[7] = lineArray[7]
            if len(lineArray[8]) == 0:
                row[8] = 0
            else:
                row[8] = lineArray[8]
        
            row[9] = int(lineArray[9])
        except Exception as e:
            print(str(e))
            continue
        try:
            x.execute("insert into RT_LeaveTimes_2016(TripId, DataSource, DayOfService, ProgrNumber, StopPointId, PlannedTime_Arr, PlannedTime_Dep, ActualTime_Arr, ActualTime_Dep, VehicleId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
            count += 1
        except Exception as e:
            print(str(e))
            print(row[3],'-',row[7],'-',row[8],'-',row[9])
            pass
        if count % 5000 == 0:
            print("Have inserted {} rows".format(count))
    conn.commit()
    x.close()

if __name__ == '__main__':
    file = "./rt_leavetimes_2016_I_DB.txt"
    #file = "./rt_leavetimes_2017_I_DB.txt"
    main(file)
