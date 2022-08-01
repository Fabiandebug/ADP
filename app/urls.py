from django.urls import path, include
from . views import first_api_call, second_api_call, covid19_data2, data_table_api
from . import views


# myurlpatterns

urlpatterns = [

    path('api1/', first_api_call.as_view(), name='First Api call'),
    path('api2/', second_api_call.as_view(), name='Second Api call'),
    path('test/<str:country>/', covid19_data2.as_view(), name='Covid19 API url'),
    path('chart/', views.testdata, name='Covid19 url'),
    path('data/table/api/', data_table_api.as_view(), name='Data Table API url'),
    path('data/table/', views.get_data_table, name='Data Table'),

]
