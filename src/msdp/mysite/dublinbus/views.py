from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse

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

def analytics(request):
    return render_to_response("Page2.html")

def flush(request):
    myflush()
    return HttpResponse("Hello, world. You're at the flush index.")


@csrf_exempt
def form_input(request): 
    if request.method=='POST':
        start=request.POST.get('Start')
        end=request.POST.get('End')
        time=request.POST.get('Time')
        reply = '{},{},{}'.format(start,end,time)
    return HttpResponse(reply)
    



