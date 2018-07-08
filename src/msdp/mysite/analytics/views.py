from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .models import Analytics as AnalyticsModel
from .forms import AnalyticsForm
from msdp.script import sqlquery
import simplejson as json

# Create your views here.
class Analytics(View):
    template_name = 'analytics.html'
    method = None

    def __init__(self, method='get_tripid'):
        self.__users = None
        self.__my = sqlquery.Sqlquery()
        self.method = method

    def get(self, request):
       
        #users = my.get_tripids_by_line(LineId, Month)
        rows = []
        return render(request, self.template_name, {
            'rows': rows,
            'LineId' : None,
            'Month' : 0
        })

    def post(self, request):
        LineId = request.POST.get('lineid', '')
        Month=request.POST.get('month','')
        if self.method == 'get_tripid':
            results = self.__my.get_tripids_by_line(LineId, Month)
            if len(results) == 0:
                return self.get(request)
            else:
                my_date = '2017-{}'.format(str(Month).zfill(2))
            rows = []
            count = 0
            trips = []
            for result in results:
                trips.append(result)
                if count % 40 == 0 and count != 0:
                    rows.append({'TripId': trips})
                    trips = []
                count += 1
            return render(request, self.template_name, {
                'rows': rows,
                'date': my_date,
            })
        elif self.method == 'get_lines':
            return self.get_lines(request)
        elif self.method == 'get_available_days':
            return self.get_available_days(request)
        elif self.method == 'get_arrivaltime':
            return self.get_arrivaltime(request)

    def get_lines(self, request):
        Month = request.POST.get('month','')
        lines = self.__my.get_lines_by_month(Month)
        if len(lines) == 0:
            return self.get(request)
        else:
            my_date = '2017-{}'.format(str(Month).zfill(2))
        return render(request, self.template_name, {
            'line_rows': lines,
            'my_date' : my_date
        })

    def get_available_days(self, request):
        TripId = request.POST.get('tripid','')
        lines = self.__my.get_available_days_by_tripid(TripId)
        if len(lines) == 0:
            return self.get(request)
        return render(request, self.template_name, {
            'date_rows': lines,
            'trip_id': TripId
        })

    def get_arrivaltime(self, request):
        TripId = request.POST.get('tripid','')
        Date = request.POST.get('date','')
        lines = self.__my.get_arrivaltime_from_tripid_and_date(TripId, Date)
        columns = ['Station NO.', 'PlannedArrTime', 'ActualArrTime']
        lines.insert(0,columns)
        print(lines)
        test = json.dumps(lines)
        if len(lines) == 0:
            return self.get(request)
        return render(request, self.template_name, {
            'arrtime_rows': test,
            'arr_trip_id': TripId,
            'arr_date': Date
        })
