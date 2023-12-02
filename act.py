import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from bokeh.plotting import figure

st.set_page_config(layout="centered")
df = pd.read_csv('police.csv')


st.title('Police incident reports from 2018 to 2020 in San Francisco')
st.markdown('The data shown below belongs to incident reports in the City of San Francisco, from the year 2018 to 2020, woth details from each case such as date, day of the week, police district, neighbourhood in which it happened, type of incident in category and subcategory, exact location and resolution')




mapa = pd.DataFrame()
mapa['Date'] = df['Incident Date']
mapa['Day'] = df['Incident Day of Week']
mapa['District'] = df['Police District']
mapa['Neighbourhood'] = df['Analysis Neighborhood']
mapa['Incident Category'] = df['Incident Category']
mapa['Incident Subcategory'] = df['Incident Subcategory']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa = mapa.dropna()


subset_data2 = mapa
police_district_input = st.sidebar.multiselect('Police District',
                                         mapa.groupby('District').count().reset_index()['District'].tolist())
if len(police_district_input) > 0:
    subset_data2 = mapa[mapa['District'].isin(police_district_input)]

subset_data1 = subset_data2
neighbourhood_input = st.sidebar.multiselect('Neighbourhood',
                                         subset_data2.groupby('Neighbourhood').count().reset_index()['Neighbourhood'].tolist())
if len(neighbourhood_input) > 0:
    subset_data1 = subset_data2[subset_data2['Neighbourhood'].isin(neighbourhood_input)]

subset_data = subset_data1
incident_input = st.sidebar.multiselect('Incident Category',
                                        subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
if len(incident_input) > 0:
    subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]

subset_data



# Calcular las métricas relevantes
total_cases = subset_data.shape[0]
resolved_cases = subset_data[subset_data['Resolution'] != 'Open or Active'].shape[0]

resolution_rate = (resolved_cases / total_cases) * 100

# Crear una nueva columna en el DataFrame para las métricas
subset_data['Resolution Rate'] = resolution_rate

# Visualizar las métricas
st.subheader('Police Department Metrics')

# 1. Índice de Resolución de Casos
c1, c2 = st.columns(2)
c1.info(f"Resolution Rate: {resolution_rate:.2f}%")
subset_data[['Resolution Rate']]




# Visualización del mapa y gráficas
st.markdown('Crime locations in San Francisco')
st.map(subset_data, color=(.1,.3,.4,.5))

st.markdown('Crimes ocurred per date')
st.bar_chart(subset_data['Date'].value_counts())

st.markdown('Types of crimes')
st.bar_chart(subset_data['Incident Category'].value_counts(),
             color = (.2,.3,.4,.5))



st.markdown('Resolution status')

labels = subset_data['Resolution'].unique()
values = subset_data['Resolution'].value_counts()

fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])

st.plotly_chart(fig)


