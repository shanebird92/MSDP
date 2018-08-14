import MySQLdb
import sys
import datetime
class Sqlquery:
    def __init__(self):
        try:
            self.__conn = MySQLdb.connect(host = "137.43.49.51",
                                          user = "student",
                                          passwd="MSDPUCD1234",
                                          db = "SummerProject")
        except Exception as e:
            print(str(e))
            return ''

    def test(self):
        print("hwllo,world!")
        return 12345
       
    def get_tripids_by_line(self, line, month):
        date = '2017-{}'.format(str(month).zfill(2))
        startDate = date + '-01'
        endDate = date + '-31'
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct TripId FROM SummerProject.RT_Trips where LineId='{}' \
                           and DayOfService BETWEEN '{}' AND '{}' ORDER BY TripId".format(line, startDate, endDate))
        except Exception as e:
            print(str(e))
            return ''
        row = x.fetchone()
        count = 0
        tripIDs = []
        while row is not None:
            count += 1
            tripIDs.append(row[0])
            row = x.fetchone()
        self.__conn.commit()
        x.close()       
        return tripIDs

    def get_tripids_by_lineMonthTime(self, line, month, timeid):
        mydate = '2017_{}'.format(str(month).zfill(2))
        start_time = (int(timeid)-1) * 3600
        end_time = (int(timeid)) * 3600
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct TripId FROM SummerProject.RT_LeaveTimesTrips_{} where LineId='{}' \
                           and PlannedTime_Arr BETWEEN {} AND {} ORDER BY TripId".format(mydate, line, start_time, end_time))
        except Exception as e:
            print(str(e))
            return ''
        row = x.fetchone()
        count = 0
        tripIDs = []
        while row is not None:
            count += 1
            tripIDs.append(row[0])
            row = x.fetchone()
        self.__conn.commit()
        x.close()
        return tripIDs


    def get_lines_by_tripid(self, tripid):
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct LineId FROM SummerProject.RT_Trips where TripId = {}".format(tripid))
        except Exception as e:
            print(str(e))
            return ''
        row = x.fetchone()
        count = 0
        lines = []
        while row is not None:
            count += 1
            lines.append(row[0])
            row = x.fetchone()
        self.__conn.commit()
        x.close()       
        return lines[0]

    def get_lines_by_month(self, month):
        date = '2017-{}'.format(str(month).zfill(2))
        startDate = date + '-01'
        endDate = date + '-31'
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct LineId FROM SummerProject.RT_Trips where DayOfService \
                           between '{}' and '{}' ORDER BY LineId".format(startDate, endDate))
        except Exception as e:
            print(str(e))
            return ''
        row = x.fetchone()
        count = 0
        lines = []
        while row is not None:
            count += 1
            lines.append(row[0])
            row = x.fetchone()
        self.__conn.commit()
        x.close()       
        return lines

    def get_available_days_by_tripid(self, tripid):
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct DayOfService FROM SummerProject.RT_LeaveTimes \
                           where TripId = {} ORDER BY DayOfService".format(tripid))
        except Exception as e:
            print(str(e))
            return ''
        row = x.fetchone()
        count = 0
        rows = []
        while row is not None:
            count += 1
            rows.append(str(row[0]))
            row = x.fetchone()
        self.__conn.commit()
        x.close()       
        return rows

    def get_available_days_by_monthTripid(self, month, tripid):
        mydate = '2017_{}'.format(str(month).zfill(2))
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct DayOfService FROM SummerProject.RT_LeaveTimesTrips_{} \
                           where TripId = {} ORDER BY DayOfService".format(mydate, tripid))
        except Exception as e:
            print(str(e))
            return ''
        row = x.fetchone()
        count = 0
        rows = []
        while row is not None:
            count += 1
            rows.append(str(row[0]))
            row = x.fetchone()
        self.__conn.commit()
        x.close()       
        return rows
    def get_available_days_by_month(self, month):
        date = '2017-{}'.format(str(month).zfill(2))
        startDate = date + '-01'
        endDate = date + '-31'
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct DayOfService FROM SummerProject.RT_LeaveTimes_2017_{} \
                           where DayOfService between '{}' and '{}' \
                               ORDER BY DayOfService".format(str(month).zfill(2), startDate, endDate))
        except Exception as e:
            print(str(e))
            return ''
        row = x.fetchone()
        count = 0
        rows = []
        while row is not None:
            count += 1
            rows.append(str(row[0]))
            row = x.fetchone()
        self.__conn.commit()
        x.close()       
        return rows

    def get_available_days_by_tripid_and_month(self, tripid, month):
        date = '2017-{}'.format(str(month).zfill(2))
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct DayOfService FROM SummerProject.RT_LeaveTimesTrips_2017_{} where  \
                           TripId='{}'".format(str(month).zfill(2), tripid))
        except Exception as e:
            print(str(e))
            return ''
        row = x.fetchone()
        count = 0
        rows = []
        new_row = None
        while row is not None:
            count += 1
            new_row = str(row[0])
            rows.append(new_row)
            row = x.fetchone()
        self.__conn.commit()
        x.close()       
        return rows


    def get_available_days_by_line_and_month(self, line, month):
        date = '2017-{}'.format(str(month).zfill(2))
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct DayOfService FROM SummerProject.RT_LeaveTimesTrips_2017_{} where \
                           LineId='{}'".format(str(month).zfill(2), line))
        except Exception as e:
            print(str(e))
            return ''
        row = x.fetchone()
        count = 0
        rows = []
        new_row = None
        while row is not None:
            count += 1
            new_row = str(row[0])
            rows.append(new_row)
            row = x.fetchone()
        self.__conn.commit()
        x.close()       
        return rows

    def get_arrivaltime_from_tripid_and_date(self, tripid, mydate):
        month = mydate.split('-')[1]
        try:
            x = self.__conn.cursor()
            x.execute("SELECT ProgrNumber, PlannedTime_Arr, ActualTime_Arr FROM SummerProject.RT_LeaveTimes_2017_{} \
                           where tripid='{}' and DayOfService = '{}' ORDER BY ProgrNumber".format(month, tripid, mydate))
        except Exception as e:
            print(str(e))
            return ''
        row = x.fetchone()
        count = 0
        rows = []
        while row is not None:
            count += 1
            rows.append(list(row))
            row = x.fetchone()
        self.__conn.commit()
        x.close()       
        return rows

    def get_ontime_times_from_line(self, line):
        try:
            x = self.__conn.cursor()
            x.execute("SELECT DayOfService, count(*) FROM SummerProject.RT_LeaveTimesTrips_2017_06 where  LineId = '{}' and PlannedTime_Arr >= ActualTime_Arr group by DayOfService order by DayOfService".format(line))
            rows = x.fetchall()
            x.execute("SELECT DayOfService, count(*) FROM SummerProject.RT_LeaveTimesTrips_2017_06 where  LineId = '{}' and PlannedTime_Arr < ActualTime_Arr group by DayOfService order by DayOfService".format(line))
            rows2 = x.fetchall()
        except Exception as e:
            print(str(e))
            return ''
        count = 0
        myrows = {}
        for row in rows:
            timestamp = row[0]
            myrows[str(timestamp)] = row[1]
        for row2 in rows2:
            timestamp = row2[0]
            myrows[str(timestamp)] = myrows[str(timestamp)]/(row2[1] + myrows[str(timestamp)])
            #myrows[str(timestamp)] = row2[1]/(row2[1] + myrows[str(timestamp)])
        self.__conn.commit()
        x.close()       
        return myrows

    def get_stoppointid_by_line(self, line, direction):
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct ProgrNumber, StopPointId FROM SummerProject.RT_LeaveTimesTrips_2017_06 \
                           where LineId='{}' and Direction={} order by ProgrNumber".format(line, direction))
        except Exception as e:
            print(str(e))
            return ''
        row = x.fetchone()
        count = 0
        lines = {}
        while row is not None:
            count += 1
            if row[0] in lines.keys():
                lines[row[0]].append(row[1])
            else:
                lines[row[0]]=[row[1]]
                
            row = x.fetchone()
        self.__conn.commit()
        x.close()       
        return lines
    
def main():
    my = Sqlquery()
    #my.test()
    #array = my.get_tripids_by_line('39A', '1')
    #array = my.get_lines_by_tripid('5012600')
    #array = my.get_lines_by_tripid('4335079')
    #for i in range(1,7):
    #    array = my.get_lines_by_month(str(i))
    #    print(array)
    #array = my.get_tripids_by_lineMonthTime('116', 2, 10)
    array = my.get_available_days_by_monthTripid(1, 5002343)
    print(array)
    #print(len(array))
    #print(len(array))
    #array = my.get_available_days_by_month(5)
    #array = my.get_available_days_by_line_and_month('39A', 6)
    #array = my.get_available_days_by_tripid_and_month('5012600', 6)
    #array = my.get_available_days_by_tripid('5012600')
    #my.get_data_from_tripid_and_date(5117245, '2017-06-01')
    #array = my.get_arrivaltime_from_tripid_and_date(5012600, '2017-06-02')
    #array = my.get_arrivaltime_from_tripid_and_date(4591857, '2017-05-12')
    #array = my.get_stoppointid_by_line('145', 1)
    #array = my.get_stoppointid_by_line('39A', 1)
    #array = my.get_ontime_times_from_line('39A')
    #array = my.get_stoppointid_by_line('45A', 2)
    #print(sorted(array.items()))

if __name__ == '__main__':
    main()
