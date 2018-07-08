from django.db import models

# Create your models here.
class Analytics(models.Model):
    TripId = models.CharField(max_length=50, primary_key=True)
    DayOfService = models.CharField(max_length=100)
    ProgrNumber = models.DateTimeField(max_length=10)
    StopPointId = models.CharField(max_length=20)
    PlannedTime_Arr = models.CharField(max_length=20)
    ActualTime_Arr = models.CharField(max_length=20)
    LineId = models.CharField(max_length=20)
    Direction = models.CharField(max_length=20)
    Month = models.CharField(max_length=20)
