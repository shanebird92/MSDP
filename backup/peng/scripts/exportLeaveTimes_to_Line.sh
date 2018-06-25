#!/bin/bash
mysql -ustudent -pMSDPUCD1234 -e "use SummerProject; select RT_LeaveTimes.* from RT_LeaveTimes, RT_Trips where RT_LeaveTimes.TripId = RT_Trips.TripId and RT_Trips.LineId = '39A' and RT_LeaveTimes.dayOfService > '2017-01-31' and RT_LeaveTimes.dayOfService < '2017-03-01'" | tr '\t' ',' > LeaveTimes_FEB_39A.csv
