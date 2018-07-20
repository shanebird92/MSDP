from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .models import Analytics as AnalyticsModel
from .forms import AnalyticsForm
from msdp.script import sqlquery
import simplejson as json
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import os

# Create your views here.
class Analytics(View):
    template_name = 'analytics.html'
    method = None

    def __init__(self, method='form_input'):
        self.__users = None
        self.__my = sqlquery.Sqlquery()
        self.method = method
        self.__data_path = os.path.dirname(os.path.abspath(__file__)) + "/../../../../data"

    def get(self, request):
        lines_json = "{}/lines.json".format(self.__data_path)
        json_data=open(lines_json).read()
        lines = json.loads(json_data)

        return render(request, self.template_name, {'Lines': json.dumps(lines)})

    def post(self, request):
        if self.method == 'form_input':
            LineId = request.POST.get('LineId')
            Month = request.POST.get('Month')
            timeID = request.POST.get('timeInterval')

            #return HttpResponse([LineId, ":", Month, ":", timeInterval])
            results = self.__my.get_tripids_by_lineMonthTime(LineId, Month, timeID)
            if len(results) == 0:
                return self.get(request)
            rows = []
            count = 1
            trips = []
            for result in results:
                trips.append(result)
                if count % 25 == 0 and count != 0:
                    rows.append({'TripId': trips})
                    trips = []
                count += 1
            json_routes = json.dumps(rows)
            return HttpResponse(json_routes)
        elif self.method == 'get_lines':
            return self.get_lines(request)
        elif self.method == 'get_days':
            tripId = request.POST.get('tripid')
            Month = request.POST.get('month')
            #return HttpResponse([tripId, ":", Month])
            days = self.__my.get_available_days_by_monthTripid(Month, tripId)
            results = {'trip_id': tripId, 'days': days}
            json_routes = json.dumps(results)
            return HttpResponse(json_routes)
        elif self.method == 'get_arrivaltime':
            return self.get_arrivaltime(request)
        elif self.method == 'get_stoppointids':
            line = request.POST.get('lineid')
            a_stoppointids = self.__my.get_stoppointid_by_line(line, 1)
            b_stoppointids = self.__my.get_stoppointid_by_line(line, 2)
            if len(a_stoppointids) == 0 and len(b_stoppointids) == 0:
                return self.get(request)
            results = {
                       'direction_a': a_stoppointids,
                       'direction_b': b_stoppointids
                      }
            #return HttpResponse([line])
            json_routes = json.dumps(results)
            return HttpResponse(json_routes)
            #return self.get_stoppointids(request)

    def get_stoppointids(self, request):
        line = request.POST.get('lineid','')
        a_stoppointids = self.__my.get_stoppointid_by_line(line, 1)
        b_stoppointids = self.__my.get_stoppointid_by_line(line, 2)
        if len(a_stoppointids) == 0 and len(b_stoppointids) == 0:
            return self.get(request)
        return render(request, self.template_name, {
            'direction_a': a_stoppointids,
            'direction_b': b_stoppointids
        })

    def get_arrivaltime(self, request):
        TripId = request.POST.get('tripid','')
        Date = request.POST.get('date','')
        lines = self.__my.get_arrivaltime_from_tripid_and_date(TripId, Date)
        columns = ['Station NO.', 'PlannedArrTime', 'ActualArrTime']
        if len(lines) == 0:
            return self.get(request)
        lines.insert(0,columns)
        test = json.dumps(lines)
        return render(request, self.template_name, {
            'arrtime_rows': test,
            'arr_trip_id': TripId,
            'arr_date': Date
        })
