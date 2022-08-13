from ast import Is
from calendar import month
from cmath import nan
from ipaddress import ip_address
from turtle import color
from urllib import request
from django.shortcuts import render
from numpy import longlong
from rest_framework.views import APIView
from django.views.generic import TemplateView
from ipware import get_client_ip
from rest_framework.response import Response
from rest_framework import status
from .models import apirates
import datetime
from django.utils import timezone
import requests
import json
import folium
import pandas as pd


# # Create your views here.


# Problem 1 - API rate-limiting

# Get user ip_address


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return(ip)


def RateLimitChecker(ip_address, url, maxrate):
    ratelimitObj = apirates.objects.filter(ip_address=ip_address, url=url)
    count = 1
    if(len(ratelimitObj) == 0):
        ratelimitObj = apirates.objects.create(
            ip_address=ip_address, url=url, count=1, maxrate=maxrate)
    else:
        ratelimitObj = ratelimitObj[0]
        current_time = timezone.localtime(timezone.now())
        timediff = current_time - ratelimitObj.lastupdated
        if(timediff < datetime.timedelta(seconds=10)):
            if(ratelimitObj.count >= ratelimitObj.maxrate):
                response_data = {
                    "success": False,
                    "message": "Api Call Rate exceeded",
                    "timediffrence": timediff
                }
                return response_data
            else:
                count = ratelimitObj.count+1
                ratelimitObj.count = count
                ratelimitObj.lastupdated = current_time
                ratelimitObj.save()
        else:
            count = 1
            ratelimitObj.count = 1
            ratelimitObj.lastupdated = current_time
            ratelimitObj.save()
    response_data = {
        "success": True,
        "message": "Success",
        "count": count
    }
    return response_data


class first_api_call(APIView):
    def post(self, request):
        ip_address = get_client_ip(request)
        maxrate = 5
        url = "http://127.0.0.1:8080/api1/"
        response_data = RateLimitChecker(ip_address, url, maxrate)
        return Response(response_data, status=status.HTTP_200_OK)


class second_api_call(APIView):
    def post(self, request):
        ip_address = get_client_ip(request)
        maxrate = 8
        url = "http://127.0.0.1:8080/api2/"
        response_data = RateLimitChecker(ip_address, url, maxrate)
        return Response(response_data, status=status.HTTP_200_OK)


# Problem 2 - Client-side general chart visualizations
# I used the RapidAPI.com platforms free open API on Covid19 data to setup my general chart visualization


def get_country_history_data(country):

    url = (f"https://covid-193.p.rapidapi.com/history?country={country}")

    headers = {
        "X-RapidAPI-Key": "9f5981b0f3msheb7c904144e3675p16a530jsn1d8c399a30d6",
        "X-RapidAPI-Host": "covid-193.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    return response


class covid19_data2(APIView):

    def get(self, request, country):

        response_data = get_country_history_data(country)
        input_data = json.loads(response_data.text)

        return Response(input_data, status=status.HTTP_200_OK)


def testdata(request):

    if request.method == "POST":
        country = request.POST['country']
        print(country)

        response_data = get_country_history_data(country)
        input_data = json.loads(response_data.text)
        working_data = input_data['response']
        new_case = []
        date = []

        for x in range(1, 30):

            country = working_data[0]['country']
            new_case.append(working_data[x]['cases']['new'])
            date.append(working_data[x]['day'])

            context = {
                "country_name": country,
                "new_case": new_case,
                "case_date": date,
            }
    else:
        country = ''
        context = {}
    return render(request, 'chart.html', context)


# Problem 3 - Client-side data table
# I used the RapidAPI.com platforms free open API on Covid19 data to setup my data table

def get_statistics(request):

    url = "https://covid-193.p.rapidapi.com/statistics"

    headers = {
        "X-RapidAPI-Key": "9f5981b0f3msheb7c904144e3675p16a530jsn1d8c399a30d6",
        "X-RapidAPI-Host": "covid-193.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    return response


class data_table_api(APIView):
    def get(self, request):
        country = []
        new_case = []
        total_cases = []
        recoverd = []
        deaths = []
        day = []

        statistics = get_statistics(request)
        response_data = json.loads(statistics.text)
        for data in response_data['response']:

            country.append(data['country'])
            new_case.append(data['cases']['new'])
            total_cases.append(data['cases']['total'])
            recoverd.append(data['cases']['recovered'])
            deaths.append(data['deaths']['total'])
            day.append(data['day'])

            context = {
                "country": country,
                "new_case": new_case,
                "total_cases": total_cases,
                "deaths": deaths,
                "date": day
            }

        return Response(context, status=status.HTTP_200_OK)


def get_data_table(request):

    country = []
    new_case = []
    total_cases = []
    recoverd = []
    deaths = []
    day = []

    statistics = get_statistics(request)
    response_data = json.loads(statistics.text)
    for data in response_data['response']:

        country.append(data['country'])
        new_case.append(data['cases']['new'])
        total_cases.append(data['cases']['total'])
        recoverd.append(data['cases']['recovered'])
        deaths.append(data['deaths']['total'])
        day.append(data['day'])

        context = zip(country, new_case, total_cases, recoverd, deaths, day)

    return render(request, 'datatable.html', {'context': context})


# Problem 4 - Client-side geo visualizaion
#  I used John Hopkins Hospital Covid 19 data as my geo visualization data
def geo_visualization(request):
    covid_df = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-28-2020.csv")

    plotdata = covid_df[['Lat', 'Long_', 'Confirmed', 'Combined_Key']]

    data = plotdata.dropna()

    data_map = folium.Map(zoom_start=100)

    for (index, row) in data.iterrows():
        folium.Circle(location=[row.loc['Lat'], row.loc['Long_']], radius=10000, color='red',
                      popup='{}\nconfirmed Cases: {} '.format(
                          row.loc['Confirmed'], row.loc['Combined_Key']), tooltip='click').add_to(data_map)

    m = data_map._repr_html_()

    context = {
        'datamap': m
    }

    return render(request, 'geovisualization.html', context)

def home(request):
    
    return render(request,'index.html')