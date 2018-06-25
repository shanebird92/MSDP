#!/bin/bash
mysql -ustudent -pMSDPUCD1234 -e "select * from SummerProject.RT_LeaveTimes where DayOfService > '2017-06-30'" | tr '\t' ',' > LeaveTimes_SECOND_HALF.csv
