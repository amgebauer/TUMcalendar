import urllib.request
from TUMCalendarTools.tumtools import tools as tumtools
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    base_url = "https://"+request.META["HTTP_HOST"]+"/exec"
    return render(request, 'templates/index.html', {'base_url': base_url})

def execute(request):
    url = request.GET.get('url', '')

    # simple proxy
    # download content from the url
    response = urllib.request.urlopen(url)
    data = response.read()
    #text = data.decode('utf-8')

    return HttpResponse(tumtools.execute(data), content_type="text/calendar")
