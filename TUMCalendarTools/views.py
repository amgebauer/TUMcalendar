import urllib.request
from TUMCalendarTools.tumtools import tools as tumtools
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    base_url = "https://"+request.META["HTTP_HOST"]+"/exec"
    return render(request, 'templates/index.html', {'base_url': base_url})

def execute(request):
    p_stud = request.GET.get('pStud', '')
    p_token = request.GET.get('pToken', '')

    if(p_stud == '' or p_token == ''):
        return HttpResponse("error")

    # simple proxy
    # download content from the url
    url = ''.join(["https://campus.tum.de/tumonlinej/ws/termin/ical?pStud=",p_stud,"&pToken=",p_token])
    print(url)
    response = urllib.request.urlopen(url)
    data = response.read()
    #text = data.decode('utf-8')

    return HttpResponse(tumtools.execute(data), content_type="text/calendar")
