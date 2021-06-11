from django.shortcuts import render

# Create your views here.
from django.urls import path
from .views import pageholder
from . import views

app_name = 'forecast'

urlpatterns=[
    path('xtremedata',views.pageholder, name="xtremedata-view"),
    path('gendataset',views.generate_dataset, name="generateDataset-view"),
    path('knngenerate',views.knngenerate, name="knnGenerate-view"),
    path('knnpredict',views.knnpredict, name="knnPredict-view"),
    path('forecastdata',views.forecaster, name="forecast-view"),
    path('linearall',views.linearall, name="linearReg-view"),

]