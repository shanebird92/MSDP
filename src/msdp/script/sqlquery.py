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
        print("Data initialized")

    def test(self):
        print("hwllo,world!")
        return 12345
       
    def get_tripids_by_line(self, line, month):
        date = '2017-{}'.format(str(month).zfill(2))
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct TripId FROM SummerProject.RT_Trips where LineId='{}' and DayOfService like '%{}-%' ORDER BY TripId".format(line, date))
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
        #print("{} rows.".format(count))
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
        print("{} rows.".format(count))
        self.__conn.commit()
        x.close()       
        return lines[0]

    def get_lines_by_month(self, month):
        date = '2017-{}'.format(str(month).zfill(2))
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct LineId FROM SummerProject.RT_Trips where DayOfService like \'%{}%\' ORDER BY LineId".format(date))
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
        print("{} rows.".format(count))
        self.__conn.commit()
        x.close()       
        return lines

    def get_available_days_by_tripid(self, tripid):
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct DayOfService FROM SummerProject.RT_LeaveTimes where TripId = {} ORDER BY DayOfService".format(tripid))
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
        print("{} rows.".format(count))
        self.__conn.commit()
        x.close()       
        return rows
    def get_available_days_by_month(self, month):
        date = '2017-{}'.format(str(month).zfill(2))
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct DayOfService FROM SummerProject.RT_LeaveTimes_2017_{} where DayOfService like '%{}-%' ORDER BY DayOfService".format(str(month).zfill(2), date))
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
        print("{} rows.".format(count))
        self.__conn.commit()
        x.close()       
        return rows

    def get_available_days_by_tripid_and_month(self, tripid, month):
        date = '2017-{}'.format(str(month).zfill(2))
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct DayOfService FROM SummerProject.RT_LeaveTimesTrips_2017_{} where  TripId='{}'".format(str(month).zfill(2), tripid))
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
            #print(new_row)
            row = x.fetchone()
        print("{} rows.".format(count))
        self.__conn.commit()
        x.close()       
        return rows


    def get_available_days_by_line_and_month(self, line, month):
        date = '2017-{}'.format(str(month).zfill(2))
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct DayOfService FROM SummerProject.RT_LeaveTimesTrips_2017_{} where  LineId='{}'".format(str(month).zfill(2), line))
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
            #print(new_row)
            row = x.fetchone()
        print("{} rows.".format(count))
        self.__conn.commit()
        x.close()       
        return rows

    def get_date_from_tripid_and_month(self, tripid, month):
        try:
            x = self.__conn.cursor()
            x.execute("SELECT distinct DayOfService FROM SummerProject.RT_LeaveTimesTrips_2017_{} where tripid='{}' ORDER BY DayOfService".format(str(month).zfill(2), tripid))
        except Exception as e:
            print(str(e))
            return ''
        row = x.fetchone()
        count = 0
        while row is not None:
            count += 1
            print(row)
            row = x.fetchone()
        print("{} rows.".format(count))
        self.__conn.commit()
        x.close()       

    def get_arrivaltime_from_tripid_and_date(self, tripid, mydate):
        month = mydate.split('-')[1]
        try:
            x = self.__conn.cursor()
            x.execute("SELECT ProgrNumber, PlannedTime_Arr, ActualTime_Arr FROM SummerProject.RT_LeaveTimes_2017_{} where tripid='{}' and DayOfService like '%{}%' ORDER BY ProgrNumber".format(month, tripid, mydate))
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
        print("{} rows.".format(count))
        self.__conn.commit()
        x.close()       
        return rows
    
def main():
    my = Sqlquery()
    #my.test()
    #array = my.get_tripids_by_line('39A', '6')
    array = my.get_lines_by_tripid('5012600')
    print(array)
    #my.get_available_days_by_month(5)
    #array = my.get_available_days_by_line_and_month('39A', 6)
    #array = my.get_available_days_by_tripid_and_month('5012600', 7)
    #array = my.get_available_days_by_tripid('5012600')
    #my.get_data_from_tripid_and_date(5117245, '2017-06-01')
    #array = my.get_arrivaltime_from_tripid_and_date(5012600, '2017-06-02')
    array = my.get_arrivaltime_from_tripid_and_date(4591857, '2017-05-12')
    print(array)
    #my.get_date_from_tripid_and_month(5012600,6)

if __name__ == '__main__':
    main()
