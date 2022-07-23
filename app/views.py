from ipaddress import ip_address
from urllib import request
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from ipware import get_client_ip
from rest_framework.response import Response
from rest_framework import status
from .models import apirates
import datetime
from django.utils import timezone
# Create your views here.

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
