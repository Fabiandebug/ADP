from django.urls import path, include
from . views import first_api_call, second_api_call, covid19_data2
from . import views


# myurlpatterns

urlpatterns = [


    path('api1/', first_api_call.as_view(), name='First Api call'),
    path('api2/', second_api_call.as_view(), name='Second Api call'),
    path('test/<str:country>/', covid19_data2.as_view(), name='Covid19 url'),
    path('chart/', views.testdata, name='Covid19 url'),

]
