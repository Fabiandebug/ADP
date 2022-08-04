from django.urls import path, include
from . views import first_api_call, second_api_call, covid19_data2, data_table_api
from . import views


# myurlpatterns

urlpatterns = [
    # Problem 1 URLS APi Limiter
    path('api1/', first_api_call.as_view(), name='First Api call'),
    path('api2/', second_api_call.as_view(), name='Second Api call'),

    # Problem 2 URLS Client-side general chart visualizations
    path('test/<str:country>/', covid19_data2.as_view(), name='Covid19 API url'),
    path('chart/', views.testdata, name='Covid19 url'),

    # Problem 3 URLS Client-side data table
    path('data/table/api/', data_table_api.as_view(), name='Data Table API url'),
    path('data/table/', views.get_data_table, name='Data Table'),

    #  Problem 4 URLS Client-side geo visualizations
    path('geo/data/map/', views.geo_visualization, name="Geo Data Map"),

]
