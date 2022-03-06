import folium
import pandas as pd

import custom_icon_death

'''
Data Source: https://covid19.who.int/info

https://gist.github.com/tadast/8827699#file-countries_codes_and_coordinates-csv

- Make own csv file with data wanted to represent
    - total cases
    - vaccination admistered
    - fully vaacinated
    - city based active covid cases (need data for this!)
        - circles (rest are color map)
'''
# Data Extraction
data_cases = pd.read_csv('WHO-COVID-19-global-table-data.csv')
data_vax = pd.read_csv('vaccination-data.csv')

tot_cases_country = list(data_cases['Name'])
tot_cases_long = list(data_cases['Long'])
tot_cases_lat = list(data_cases['Lat'])
tot_cases = list(data_cases['Cases - cumulative total'])
tot_deaths = list(data_cases['Deaths - cumulative total'])

vax_country = list(data_vax['COUNTRY'])
full_vax = list(data_vax['PERSONS_FULLY_VACCINATED'])
tot_vax = list(data_vax['TOTAL_VACCINATIONS'])
date_vax = list(data_vax['DATE_UPDATED'])
tot_vax_long = list(data_vax['LONG'])
tot_vax_lat = list(data_vax['LAT'])

# Layer 1 - Map Template
map = folium.Map(location = [20, 0], zoom_start = 3, tiles = 'Stamen Terrain')
# 'CartoDB dark_matter' 'Stamen Terrain'

# Map Total Cases Layer
fg_tot_cases = folium.FeatureGroup(name = 'Cummulative COVID-19 Cases')

# Map Total Deaths Layer
fg_tot_deaths = folium.FeatureGroup(name = 'Cummulative COVID-19 Deaths')

# Map Vaccinated Data Layer
fg_vax = folium.FeatureGroup(name = 'Total Vaccinations Globally')

# Map of Population Layer
fg_pop = folium.FeatureGroup(name = 'Population (from 2005)')

def color_cases (num):
    if num >= 5000000:
        return 'purple'
    elif 100000 <= num < 5000000:
        return 'blue'
    else:
        return 'lightgreen'

def vax_status(tot, full):
    if (full/tot <= 0.5):
        return 'Poor!'
    elif (0.5 < full/tot <= 0.75):
        return 'Moderate'
    else:
        return 'Excellent!'

# For stylized text in the popup window
html_1 = """
<h4><u>COVID-19 Vaccination Data for <br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s<a>:</u></br></h4>
<p><b><i>Total Administered Vaccinations:</b></i> %s </p>
<p><b><i>Total Fully Vaccinated Indivduals:</b></i> %s as of %s </p>
<p><b>Vaccination Status: %s </b></p>
"""

html_2 = """
<h4><u>Total COVID-19 Cases as of 02/12/2022 in %s:</h4></u> %s
"""

for lt, lg, num, ctry in zip(tot_cases_lat, tot_cases_long, tot_cases, tot_cases_country):
    # text = folium.Html(html_2 % (ctry, tot_cases))#, script = True, width = 200, height = 300)
    fg_tot_cases.add_child(folium.CircleMarker(location = [lt, lg], radius = 15, tooltip = 'Total COVID-19 Cases as of 02/12/2022 in ' + str(ctry) + ': ' + '{:,}'.format(num),
    fill_color = color_cases(int(num)), color = 'beige', fill = True, fill_opacity = 0.5))

for lt, lg, num, ctry in zip(tot_cases_lat, tot_cases_long, tot_deaths, tot_cases_country):
    icon = folium.features.CustomIcon(custom_icon_death.url, icon_size = (20,20))
    fg_tot_deaths.add_child(folium.Marker([lt, lg], tooltip = 'Total COVID-19 Deaths as of 02/12/2022 in ' + str(ctry) + ': ' + str(num), icon = icon)).add_to(map)

'''
    fg_tot_deaths.add_child(folium.CircleMarker(location = [lt, lg], radius = 5, popup = 'Total COVID-19 Deaths as of 02/12/2022 in ' + str(ctry) + ': ' + str(num),
    fill_color = 'red', color = 'beige', fill = True, fill_opacity = 0.5))

    if num >= 1000000:
        fg_tot_cases.add_child(folium.Marker(location = [lt, lg], popup = 'Cummulative COVID-19 Cases: ' + str(num), icon = folium.Icon(color = 'blue', icon = 'info-sign'))).add_to(map)
    elif 50000 <= num < 1000000:
        fg_tot_cases.add_child(folium.Marker(location = [lt, lg], popup = 'Cummulative COVID-19 Cases: ' + str(num), icon = folium.Icon(color = 'green', icon = 'info-sign'))).add_to(map)
    else:
        fg_tot_cases.add_child(folium.Marker(location = [lt, lg], popup = 'Cummulative COVID-19 Cases: ' + str(num), icon = folium.Icon(color = 'purple', icon = 'info-sign'))).add_to(map)
'''

for lt, lg, tot, full, date, ctry in zip(tot_vax_lat, tot_vax_long, tot_vax, full_vax, date_vax, vax_country):
    status = vax_status(tot, full)
    iframe = folium.IFrame(html = html_1 % (ctry, ctry, "{:,}".format(tot), "{:,}".format(full), date, status), width = 300, height = 200)
    if (full/tot <= 0.5):
        fg_vax.add_child(folium.Marker([lt,lg], popup = folium.Popup(iframe), icon = folium.Icon(color = "darkred")))
    elif (0.5 < full/tot <= 0.75):
        fg_vax.add_child(folium.Marker([lt,lg], popup = folium.Popup(iframe), icon = folium.Icon(color = "orange")))
    else:
        fg_vax.add_child(folium.Marker([lt,lg], popup = folium.Popup(iframe), icon = folium.Icon(color = "darkgreen")))

    # iframe = folium.IFrame(html = html_1 % (ctry, ctry, tot, full, date, status), width = 300, height = 300)
    # fg_vax.add_child(folium.CircleMarker(location = [lt, lg], radius = 10, popup = 'Total Vaccinations Administered: ' + str(tot) + '\n' + 'Fully Vaccinated People: ' + str(full) + ' as of ' + str(date),
    # fill_color = color_vax(tot, full), color = 'beige', fill = True, fill_opacity = 0.7))
    # fg_vax.add_child(folium.Marker([lt,lg], popup = folium.Popup(iframe), icon = folium.Icon(color = "green")))

# creates a GeoJson object and for GeoJson data
# lambda allows you to write a function in a single line
fg_pop.add_child(folium.GeoJson(data = open('world.json', 'r', encoding = 'utf-8-sig').read(),
style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'lightblue' if 10000000 < x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fg_tot_cases)
map.add_child(fg_vax)
map.add_child(fg_tot_deaths)
map.add_child(fg_pop)

map.add_child(folium.LayerControl())

map.save('COVID-19 Map.html')
