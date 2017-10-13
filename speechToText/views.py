from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf

'''def speechToText(request):
    template = get_template('index.html')

    context = {}
    #context.update(csrf(request))
    return HttpResponse(template.render(context))'''

'''def speechToText(request):
    #candidates = Candidate.objects.all()
    return render(request, 'speechToText/index.html')'''

def speechToText(request):
    template = get_template('index.html')
    context={}
    return HttpResponse(template.render(context))

'''def speechToText(request):
    return HttpResponse("Hello, world. You're at the polls index.")'''