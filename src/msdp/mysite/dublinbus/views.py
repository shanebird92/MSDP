from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import requests, json, os

# Create your views here.
from django.core.cache import cache # This is the memcache cache.
from django.db import connections, transaction
from django.views.decorators.csrf import csrf_exempt,csrf_protect

# Import python modules
from msdp.script import ann, weather, changeBus

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
def transfer_form_input(request): 
    data_path = os.path.dirname(os.path.abspath(__file__)) + "/../../../../data"
    try:
        station_json_file = '{}/stopToStationName.json'.format(data_path)
        all_stations = json.loads(open(station_json_file).read())
        gps_json_file = '{}/stop_latlong.json'.format(data_path)
        all_gps = json.loads(open(gps_json_file).read())
    except Exception as e:
        all_stations = {}
        all_gps = {}

    if request.method == 'POST':
        start = int(request.POST.get('Start'))
        end = int(request.POST.get('End'))
        mytime = int(request.POST.get('Time'))
        forecastdate = request.POST.get('Date')
        
        # By default: rain is 0, sun is 0 
        my = weather.Weather()
        [rain, sun] = my.get_weather_info(forecastdate)
        # Get solution for transferring-buses
        my = changeBus.ChangeBus(start, end, mytime, rain, sun)
        solution = my.getFinalRoute()
        route = {}
        route['walk1_startID'] = solution[0]
        route['walk1_start_station'] = all_stations[str(solution[0])].strip()
        route['first_stop_location'] = all_gps[str(solution[0])]

        route['walk1_endID'] = solution[1]
        route['walk1_end_station'] = all_stations[str(solution[1])].strip()

        route['walk1_distance'] = solution[2]
        route['lineA'] = solution[3][0]['firstLines']

        route['middle_walk_startID'] = solution[3][0]['firstLineTransferStop']
        route['middle_walk_start_station'] = all_stations[str(solution[3][0]['firstLineTransferStop'])].strip()

        route['middle_walk_endID'] = solution[3][0]['secondLineTransferStop']
        route['middle_walk_end_station'] = all_stations[str(solution[3][0]['secondLineTransferStop'])].strip()

        route['middle_walk_distance'] = solution[3][0]['transferDistance']
        route['lineB'] = solution[3][0]['secondLines']

        route['walk2_startID'] = solution[4]
        route['walk2_start_station'] = all_stations[str(solution[4])].strip()

        route['walk2_endID'] = solution[5]
        route['walk2_end_station'] = all_stations[str(solution[5])].strip()
        route['last_stop_location'] = all_gps[str(solution[5])]

        route['walk2_distance'] = solution[6]

        json_route = json.dumps(route)
        return HttpResponse(json_route)
    else:
        return 1
