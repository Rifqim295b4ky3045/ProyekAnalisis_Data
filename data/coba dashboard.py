import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df_day = pd.read_csv('day.csv') 
df_hour = pd.read_csv('hour.csv')

# Title
st.title('Dashboard Rental Sepeda')

# Sidebar untuk input pengguna
st.sidebar.header('Pengaturan Visualisasi')
data_choice = st.sidebar.selectbox("Pilih data yang ingin ditampilkan:", ["Data Harian", "Data Jam"])

# Pilihan data
if data_choice == "Data Harian":
    data = day_data
else:
    data = hour_data

# Input dari pengguna
st.sidebar.subheader("Filter Berdasarkan Waktu:")
start_date = st.sidebar.date_input('Pilih tanggal mulai', value=pd.to_datetime(data['dteday']).min())
end_date = st.sidebar.date_input('Pilih tanggal akhir', value=pd.to_datetime(data['dteday']).max())
filtered_data = data[(pd.to_datetime(data['dteday']) >= pd.to_datetime(start_date)) & 
                     (pd.to_datetime(data['dteday']) <= pd.to_datetime(end_date))]

# Input untuk parameter visualisasi tren
st.sidebar.subheader("Filter Berdasarkan Kondisi Cuaca:")
weather_choice = st.sidebar.multiselect("Pilih kondisi cuaca:", filtered_data['weathersit'].unique())

if weather_choice:
    filtered_data = filtered_data[filtered_data['weathersit'].isin(weather_choice)]

# Input untuk suhu
min_temp = st.sidebar.slider('Suhu minimum:', min_value=float(data['temp'].min()), max_value=float(data['temp'].max()), value=float(data['temp'].min()))
max_temp = st.sidebar.slider('Suhu maksimum:', min_value=float(data['temp'].min()), max_value=float(data['temp'].max()), value=float(data['temp'].max()))
filtered_data = filtered_data[(filtered_data['temp'] >= min_temp) & (filtered_data['temp'] <= max_temp)]

# Visualisasi tren penggunaan sepeda berdasarkan waktu, cuaca, dan suhu
st.subheader("Tren Penggunaan Sepeda")
st.line_chart(filtered_data[['dteday', 'cnt']].set_index('dteday'))

# Pilihan parameter untuk visualisasi korelasi
st.sidebar.subheader("Visualisasi Korelasi")
param1 = st.sidebar.selectbox('Pilih parameter pertama:', filtered_data.columns)
param2 = st.sidebar.selectbox('Pilih parameter kedua:', filtered_data.columns)

# Visualisasi korelasi antara 2 parameter
if param1 and param2:
    st.subheader(f'Korelasi antara {param1} dan {param2}')
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_data, x=param1, y=param2, ax=ax)
    st.pyplot(fig)

# Menampilkan data yang sudah difilter
st.subheader("Data yang Ditampilkan")
st.dataframe(filtered_data)
