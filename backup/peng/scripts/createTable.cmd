CREATE TABLE SummerProject.RT_LeaveTimes_201703 (
	TripId INT(11),
	DataSource VARCHAR(45), 
        DayOfService DATE,
        ProgrNumber INT(11),
        StopPointId INT(11),
        PlannedTime_Arr INT(11),
        PlannedTime_Dep INT(11),
        ActualTime_Arr INT(11),
        ActualTime_Dep INT(11),
        VehicleId INT(11),
        Passengers INT(11),
        Passengersin INT(11),
        Distance INT(11),
        Suppressed VARCHAR(45),
        JustificationId INT(11),
        LastUpdate DATETIME,
        Note VARCHAR(45)
	)
