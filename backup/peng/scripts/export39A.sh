#!/bin/bash
mysql -ustudent -pMSDPUCD1234 -e "use SummerProject; select * from RT_LeaveTimes_2017_01 where RT_LeaveTimes_2017_01.TripId = any (select DISTINCT TripId from SummerProject.RT_Trips where RT_Trips.LineId = '39A' and Direction = 1)" | tr '\t' ',' > 39A_JAN_direction_1.csv
