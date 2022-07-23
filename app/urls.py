from django.urls import path, include
from . views import first_api_call, second_api_call


# myurlpatterns

urlpatterns = [

    path('api1/', first_api_call.as_view(), name='First Api call'),
    path('api2/', second_api_call.as_view(), name='Second Api call'),
]
