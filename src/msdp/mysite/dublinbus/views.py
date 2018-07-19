from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from msdp.script import ann
import json

# Create your views here.
from django.core.cache import cache # This is the memcache cache.
from django.db import connections, transaction
from django.views.decorators.csrf import csrf_exempt,csrf_protect

def myflush():
    # This works as advertised on the memcached cache:
    cache.clear()
    # This manually purges the SQLite cache:
    cursor = connections['cache_database'].cursor()
    cursor.execute('DELETE FROM cache_table')
    transaction.commit_unless_managed(using='cache_database')

def index(request):
    return render_to_response("Page1.html")

def flush(request):
    myflush()
    return HttpResponse("Hello, world. You're at the flush index.")


@csrf_exempt
def form_input(request): 
    if request.method=='POST':
        start=int(request.POST.get('Start'))
        end=int(request.POST.get('End'))
        time=int(request.POST.get('Time'))

        # Default values for Rain and Sun
        # 1 is rain/sun, 0 is non-rain or non-run
        rain = 0
        sun = 0
        # start = 1913, end = 1660
        my = ann.Ann(start, end, time, rain, sun)
        results = my.get_all_prediction()
        routes = []
        for row in results:
            route = {}
            route['line'] = row['line']
            route['traveltime'] = row['travelTime']
            route['starttime'] = row['startTime']
            route['pairarrtime'] = row['pairArrTime']
            route['pairstops'] = row['pairStops']
            route['locations'] = row['locations']
            routes.append(route)
        json_routes=json.dumps(routes)
        return HttpResponse(json_routes)
        #return render(request,'Page1.html',{'Routes':json.dumps(routes)})
    else:
        return 1

