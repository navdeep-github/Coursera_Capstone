#!/usr/bin/env python
# coding: utf-8

# In[29]:


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


# In[30]:


#Delete Borough where value is 'Not Assigned'
df_canada = canada_df[canada_df['Borough'] != 'Not assigned']
df_canada.head(10)


# In[31]:


#Groupby Neighborhood according to Postal code and separate it with comma , because one postal code can have multiple neighborhood
df_canada["Neighborhood"] = df_canada.groupby("Postal Code")["Neighborhood"].transform(lambda neigh: ', '.join(neigh))

# Drop duplicate values
canada_df = canada_df.drop_duplicates()

# Update index to be postcode
if(canada_df.index.name != 'Postal Code'):
    canada_df = canada_df.set_index('Postal Code')
    
canada_df.head(15)


# In[32]:


# Replace neighorhood value with borough column  value where there is no value in Neighorhood 
df_canada['Neighborhood'].replace("Not assigned", df_canada["Borough"],inplace=True)
df_canada.head(8)


# In[36]:


print('Dimension of Dataframe is ',df_canada.shape)


# <h1> Question Second of Assignment

# In[41]:


# Combining spatial file and data frame df_canada

geo_toronto = "https://cocl.us/Geospatial_data"

get_ipython().system("wget r'toronto_m.geospatial_data.csv' geo_toronto")

geo_toronto_data = pd.read_csv(geo_toronto).set_index('Postal Code')

geo_toronto_data.head()


# In[43]:


# Joining Canada Dataframe file with GeoSpatial file that we read into geo_toronto_data

combined_dataframe = df_canada.join(geo_toronto_data)

combined_dataframe.head(15)


# In[ ]:




