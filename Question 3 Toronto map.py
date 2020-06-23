#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

# Getting HTML page from Wiki and creationg Beautiful Soup package object
main_file_fromWiki = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")
soup_object = BeautifulSoup(main_file_fromWiki.text, 'lxml')

# Extracting table from Wiki file and saving in lists
data = []
columns = []
table = soup_object.find(class_='wikitable')
for index, tr in enumerate(table.find_all('tr')):
    section = []
    for td in tr.find_all(['th','td']):
        section.append(td.text.rstrip())
    
    #First row is columns headings
    if (index == 0):
        columns = section
    else:
        data.append(section)

#convert list into Pandas DataFrame
df_canada = pd.DataFrame(data = data, columns = columns)
df_canada.head()


# In[4]:


#Delete Borough where value is 'Not Assigned'
df_canada = df_canada[df_canada['Borough'] != 'Not assigned']
df_canada.head(10)


# In[7]:


#Groupby Neighborhood according to Postal code and separate it with comma , because one postal code can have multiple neighborhood
df_canada["Neighborhood"] = df_canada.groupby("Postal Code")["Neighborhood"].transform(lambda neigh: ', '.join(neigh))

# Drop duplicate values
df_canada = df_canada.drop_duplicates()

# Update index to be postcode
if(df_canada.index.name != 'Postal Code'):
    df_canada = df_canada.set_index('Postal Code')
    
df_canada.head(15)


# In[8]:


# Replace neighorhood value with borough column  value where there is no value in Neighorhood 
df_canada['Neighborhood'].replace("Not assigned", df_canada["Borough"],inplace=True)
df_canada.head(8)


# In[9]:


print('Dimension of Dataframe is ',df_canada.shape)


# <h1> Question Second of Assignment

# In[10]:


# Combining spatial file and data frame df_canada

geo_toronto = "https://cocl.us/Geospatial_data"

get_ipython().system("wget r'toronto_m.geospatial_data.csv' geo_toronto")

geo_toronto_data = pd.read_csv(geo_toronto).set_index('Postal Code')

geo_toronto_data.head()


# In[12]:


# Joining Canada Dataframe file with GeoSpatial file that we read into geo_toronto_data

combined_dataframe = df_canada.join(geo_toronto_data)

combined_dataframe.head(10)


# In[13]:


get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')


# In[16]:


get_ipython().system('conda install -c conda-forge geopy --yes')
from geopy.geocoders import Nominatim # Converting address into geographical data
import requests # Handle requests


import folium # map rendering library

print('Libraries imported.')


# In[17]:


combined_dataframe.head()


# <h1> Creationg map of Toronto

# In[22]:


toronto_latitude = 43.6532; toronto_longitude = -79.3832
map_toronto = folium.Map(location = [toronto_latitude, toronto_longitude], zoom_start = 10.7)

# add markers to map
for lat, lng, borough, neighborhood in zip(combined_dataframe['Latitude'], combined_dataframe['Longitude'], combined_dataframe['Borough'], combined_dataframe['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7).add_to(map_toronto)  
    

map_toronto.save("my_map1.html" )

from IPython.display import HTML

HTML('<iframe src=my_map1.html width=700 height=450></iframe>')


# In[ ]:




