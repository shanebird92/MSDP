from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import requests, json

# Create your views here.
from django.core.cache import cache # This is the memcache cache.
from django.db import connections, transaction
from django.views.decorators.csrf import csrf_exempt,csrf_protect

# Import python modules
from msdp.script import ann, weather

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
    if request.method == 'POST':
        start = int(request.POST.get('Start'))
        end = int(request.POST.get('End'))
        mytime = int(request.POST.get('Time'))
        forecastdate = request.POST.get('Date')
        
        # By default: rain is 0, sun is 0 
        my = weather.Weather()
        [rain, sun] = my.get_weather_info(forecastdate)

        # testcase: start = 1913, end = 1660
        my = ann.Ann(start, end, mytime, rain, sun)
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
        json_routes = json.dumps(routes)
        return HttpResponse(json_routes)
        #return render(request,'Page1.html',{'Routes':json.dumps(routes)})
    else:
        return 1

@csrf_exempt
def login(request): 
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        res={}
        if username=='MSDP' and password=='MSDP':
            res['info']='Successful'
        elif username!='MSDP':
            res['info']='Wrong Username'
        else:
            res['info']='Wrong Password'
           
        json_res=json.dumps(res)
        return HttpResponse(json_res)
            
        '''
        json_routes = json.dumps(username)
        return render(request,'analytics.html')
        #return render(request,'Page1.html',{'Routes':json.dumps(routes)})
        '''
    else:
        return 1

