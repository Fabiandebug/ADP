from ast import Is
from asyncio.windows_events import NULL
from calendar import month
from ipaddress import ip_address
from urllib import request
from django.shortcuts import render
from rest_framework.views import APIView
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from ipware import get_client_ip
from rest_framework.response import Response
from rest_framework import status
from .models import apirates
import datetime
from django.utils import timezone
import requests
import json
from requests.exceptions import ConnectionError
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


def get_country_history_bydate_date(country, date):
    url = (
        f"https://covid-193.p.rapidapi.com/history?country={country}&amp;day={date}")

    headers = {
        "X-RapidAPI-Key": "9f5981b0f3msheb7c904144e3675p16a530jsn1d8c399a30d6",
        "X-RapidAPI-Host": "covid-193.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    return response.json()


class covid19_data2(APIView):

    def get(self, request, country):

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
                "date": date,
            }

        return Response(context, status=status.HTTP_200_OK)


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
