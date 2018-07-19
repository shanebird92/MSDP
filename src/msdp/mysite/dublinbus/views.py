from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from msdp.script import ann
import requests
import json
import time
import datetime

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
        forecastdate=request.POST.get('Date')
        
        #calculate the time interval
        y2,m2,d2=forecastdate.split('-')
        y1=datetime.datetime.now().year
        m1=datetime.datetime.now().month
        d1=datetime.datetime.now().day
        currenttime=datetime.datetime(y1,m1,d1)
        forecasttime=datetime.datetime(int(y2),int(m2),int(d2))
        time_difference=(forecasttime-currenttime).days

        # get weather features
        # Default values for Rain and Sun
        # 1 is rain/sun, 0 is non-rain or non-sun
        weather=requests.get('http://api.openweathermap.org/data/2.5/forecast/daily?id=7778677&mode=json&units=metric&cnt=5&APPID=19b104f014c41d11939f615df3a80edf').json()
        if (time_difference>=0 and time_difference<=4):
            weather_info=weather['list'][time_difference]['weather'][0]['main']
            #key:weather description; value: rain sun
            weather_dic={'Clouds':[0,0],'Drizzle':[1,0],'Clear':[0,1],'Fog':[0,0],'Mist':[0,0],'Rain':[1,0],'Snow':[1,0],'Thundestorm':[1,0]}
            try:
                rain,sun=weather_dic.get(weather_info)
            except TypeError:
                rain=0
                sun=0
        else:
            rain=0
            sun=0
            
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

