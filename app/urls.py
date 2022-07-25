from django.urls import path, include
from . views import first_api_call, second_api_call, covid19_data


# myurlpatterns

urlpatterns = [


    # path('api1/', first_api_call.as_view(), name='First Api call'),
    # path('api2/', second_api_call.as_view(), name='Second Api call'),
    path('covid19/<str:country>/', covid19_data.as_view(), name='Covid19 url'),

]
