import pandas as pd
import requests
import json
import folium


def get_visualization_data():

    url = "https://covid-193.p.rapidapi.com/statistics"

    headers = {
        "X-RapidAPI-Key": "9f5981b0f3msheb7c904144e3675p16a530jsn1d8c399a30d6",
        "X-RapidAPI-Host": "covid-193.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    return response


def geo_visualization(request):
    country = []
    new_case = []
    active_case = []
    recovered = []
    deaths = []
    date = []

    data = get_visualization_data()
    working_data = json.loads(data.text)

    for data in working_data['response']:
        country.append(data['country'])
        new_case.append(data['cases']['new'])
        active_case.append(data['cases']['active'])
        recovered.append(data['cases']['recovered'])
        deaths.append(data['deaths']['total'])
        date.append(data['day'])

    context = {'country': country,
               'new_case': new_case,
               'active_case': active_case,
               'recovered': recovered,
               'deaths': deaths,
               'date': date,
               }

    df = pd.DataFrame(context)

    world_geo = r'templates/custom.geo.json'

    data_map = folium.Map()

    folium.Choropleth(
        # The GeoJSON data to represent the world country
        geo_data=world_geo,
        data=df,

        columns=['country', 'active_case'],
        key_on='feature.properties.name',
        threshold_scale=[0, 10, 50, 100, 500, 1000,
                         5000, 10000, 20000, 50000, 80000, 100000],
        fill_color='YlOrRd',
        fill_opacity=0.5,
        line_opacity=0.2,
        legend_name='World Covid19 cases',
        nan_fill_color='white'
    ).add_to(data_map)

    # m = data_map._repr_html_()

    # context = {
    #     'datamap': m
    # }

    # return render(request, 'geovisualization.html', context)
    data_map.save(r'./templates/map.html')
