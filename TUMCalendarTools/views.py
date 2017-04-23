import urllib.request
from TUMCalendarTools.tumtools import tools as tumtools
from django.http import HttpResponse

def index(request):
    baseurl = "https://"+request.META["HTTP_HOST"]+"/TUMcalendar/exec"
    return HttpResponse("Hello, use this base url: "+baseurl)

def execute(request):
    url = request.GET.get('url', '')

    # simple proxy
    # download content from the url
    response = urllib.request.urlopen(url)
    data = response.read()
    #text = data.decode('utf-8')

    return HttpResponse(tumtools.execute(data), content_type="text/calendar")
