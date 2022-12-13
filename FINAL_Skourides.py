"""
Class: CS230--Section 2
Name: Trianna Skourides
Description: Final Project - Boston Crime
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student. 
"""
import streamlit as st
import pandas as pd

SIDEBAR_OPTIONS = ['Home Page', 'Map of Crimes', 'Dates of Crimes', 'Bar Charts', 'Crime on your Street']

def homepage():
    st.markdown(""" <style> .font {font-size:50px ; font-family: 'Cooper Black'; color: blue;} </style> """, unsafe_allow_html=True)
    st.markdown("<p class='font'>Welcome to Trianna's Final Project on Boston Crime</p>", unsafe_allow_html=True)
    st.subheader('by Trianna Skourides for CS230')
    st.markdown(""" <style> .font2 {font-size:18px ; font-family: 'Cooper Black'; color: blue;} </style> """, unsafe_allow_html=True)
    st.markdown("<p class='font2'>Bentley University</p>", unsafe_allow_html=True)
    st.image('BPD.jpg')
    st.write('On this website, you will see the data for Boston Crimes in 2021 sorted and displayed in meaningful ways.')
    st.write('The tab called "Map of Crimes" will show the crimes on a map and the user is able to view the data on the map by district.')
    st.write('The tab called "Dates of Crimes" will have the data sorted in ascending order by the date of the crime.')
    st.write('The tab called "Bar Charts" will show multiple bar charts depicting different elements of the data.')
    st.write('Please enjoy the site.')


def sidebar():
    st.sidebar.title("Choose where to Navigate:")
    selection = st.sidebar.selectbox("Tabs", SIDEBAR_OPTIONS)
    return selection


def read_data():
    df = pd.read_csv("Boston_Crime_Date.csv",
                     header=0,
                     names=["Incident Number", "Offense Code", "Offense Code Group",
                            "Offense Description", "District", "Reporting Area", "Shooting",
                            "Date", "Year", "Month", "Day of Week", "Hour", "UCR Part",
                            "Street", "lat", "lon", "Location"])
    df["Date"] = pd.to_datetime(df['Date'],format="%m/%d/%Y %H:%M")
    return df


def read_data_district():
    df_district = pd.read_csv("Boston_Crime_Date.csv",
                     header=0,
                     names=['District', 'District Name'])

    return df_district, district_list


def district_list():
    df_district = pd.read_csv("Boston_Crime_Date.csv",
                     header=0,
                     names=['District', 'District Name'])
    list1 = df_district['District Name'].values.tolist()
    return list1


def map(df, district):
    df.index = df['District']
    df = df[['lat', 'lon']]
    df = df.loc[[district]]
    return df

def make_map(df):
    st.header('The map below shows crimes based on your district selection.')
    st.caption("Use the selection bar to pick which district's crimes you would like to view.")
    st.map(df)


def dates(df):
    data_table = df[["Incident Number", "Offense Description", "Date"]]
    st.subheader("Data Table on crimes based on date:")
    st.dataframe(data_table)
    return df


def barcharts(df):
    st.sidebar.write("Choose how you would like to see the data sorted:")
    sel_sort = st.sidebar.radio("Options:", ("Day of Week", "Month", "Offense Description", "Offense Code"))
    sorted = df.groupby(sel_sort).count()['Incident Number']
    st.subheader(f'Crime Sorted by {sel_sort}:')
    st.bar_chart(sorted)
    return df


def street(df):
    st.subheader('Below shows the entire dataset. Use the text input box below to filter the data based on street name.')
    df2 = df[['Incident Number', 'Date', "Street"]]
    st.write(df2)
    strInput = st.text_input('Type in your Street Name to see Crimes Committed there: ')
    df3 = df2.query("Street == @strInput")
    st.write(df3)

    return df


df = read_data()
selection = sidebar()
if selection == "Home Page":
    homepage()
elif selection == "Map of Crimes":
    dist = st.selectbox('Pick which district you would like to view: ', ['B2', 'D4', 'C11', 'A1', 'B3', 'C6', 'D14', "E18", "E13", 'E5', 'A7', 'A15'])
    data = map(df, dist)
    make_map(data)
elif selection == "Dates of Crimes":
    dates(df)
elif selection == "Bar Charts":
    barcharts(df)
elif selection == 'Crime on your Street':
    street(df)
