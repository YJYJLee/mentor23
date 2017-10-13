from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^speechToText/$', views.speechToText),
    url(r'^$', views.speechToText, name='speechToText'),
]