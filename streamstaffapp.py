#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Static Plots
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Dashboard Frameworks
import streamlit as st

# Date and Time
from datetime import datetime, timedelta
import pytz
from dateutil import parser
import arrow
import plotly.express as px
import re


# In[2]:


df_kit = pd.read_csv('kitting errors data.csv', encoding='latin1') 
df_kit.head()


# In[3]:


df_asl = pd.read_csv('Assembly training data.csv', encoding='latin1') 
df_asl.head()


# In[4]:


column_names_df = pd.DataFrame(df_kit.columns, columns=["Column Names"])
column_names_df.head(20)


# In[5]:


# Convert 'DAY' to datetime for both dataframes
df_kit['DAY'] = pd.to_datetime(df_kit['DAY'])
df_asl['DAY'] = pd.to_datetime(df_asl['DAY'])

# Streamlit app
st.title('STAFF PERFORMANCE ANALYSIS')

# Sidebar filters
st.sidebar.header('Filters')

# Section selection
selected_section = st.sidebar.radio(
    'Select Section to View',
    options=['Kitting', 'Assembly']
)

if selected_section == 'Kitting':
    st.header('DAILY KITTING ERRORS')

    # Kitting filters
    st.sidebar.subheader('Kitting Filters')
    selected_date_kit = st.sidebar.date_input(
        'Select a date (Kitting)',
        min_value=df_kit['DAY'].min(),
        max_value=df_kit['DAY'].max(),
        value=df_kit['DAY'].min()
    )
    selected_week_kit = st.sidebar.selectbox(
        'Select a week (Kitting)',
        options=df_kit['WEEK'].unique(),
        index=0
    )

    # Filter kitting data
    filtered_kit_df = df_kit[(df_kit['DAY'] == pd.to_datetime(selected_date_kit)) & 
                             (df_kit['WEEK'] == selected_week_kit)]

    if not filtered_kit_df.empty:
        # Group by 'NAME' and sum 'ERROR RATE'
        name_counts_kit = filtered_kit_df.groupby('NAME')['ERROR RATE'].sum().reset_index()

        # Create the bar chart
        st.bar_chart(name_counts_kit.set_index('NAME'))

        # Display the table below the bar chart
        st.table(filtered_kit_df[['NAME', 'STATION', 'ERROR', 'ERROR RATE']])
    else:
        st.write('No data available for the selected date and week in Kitting.')

elif selected_section == 'Assembly':
    st.header('DAILY ASSEMBLY ERRORS')

    # Assembly filters
    st.sidebar.subheader('Assembly Filters')
    selected_date_asl = st.sidebar.date_input(
        'Select a date (Assembly)',
        min_value=df_asl['DAY'].min(),
        max_value=df_asl['DAY'].max(),
        value=df_asl['DAY'].min()
    )
    selected_week_asl = st.sidebar.selectbox(
        'Select a week (Assembly)',
        options=df_asl['WEEK'].unique(),
        index=0
    )

    # Filter assembly data
    filtered_asl_df = df_asl[(df_asl['DAY'] == pd.to_datetime(selected_date_asl)) & 
                             (df_asl['WEEK'] == selected_week_asl)]

    if not filtered_asl_df.empty:
        # Group by 'NAME' and sum 'ERROR RATE'
        name_counts_asl = filtered_asl_df.groupby('NAME')['ERROR RATE'].sum().reset_index()

        # Create the bar chart
        st.bar_chart(name_counts_asl.set_index('NAME'))

        # Display the table below the bar chart
        st.table(filtered_asl_df[['NAME', 'STATION', 'ERROR', 'ERROR RATE']])
    else:
        st.write('No data available for the selected date and week in Assembly.')



# In[ ]:




