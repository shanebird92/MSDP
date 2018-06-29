#!/bin/bash
#mysql -ustudent -pMSDPUCD1234 -e "select * from SummerProject.RT_Trips where dayOfService < '2017-02-01'" | tr '\t' ',' > /tmp/trips.log
mysql -ustudent -pMSDPUCD1234 -e "select * from SummerProject.H_Weather" | tr '\t' ',' > ./Weather.csv
