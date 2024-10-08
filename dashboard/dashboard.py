import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
file_path = 'main_data.csv'  # Gantilah dengan path file aslimu
data = pd.read_csv(file_path)

# Convert 'dteday' to datetime
data['dteday'] = pd.to_datetime(data['dteday'])

# Sidebar filters
st.sidebar.header('Filter Options')

# Date range filter
start_date = st.sidebar.date_input('Start date', data['dteday'].min())
end_date = st.sidebar.date_input('End date', data['dteday'].max())

# Weather filter
weather_options = st.sidebar.multiselect(
    'Select Weather Condition',
    options=data['weathersit'].unique(),
    default=data['weathersit'].unique()
)

# Filter data based on user inputs
filtered_data = data[
    (data['dteday'] >= pd.to_datetime(start_date)) & 
    (data['dteday'] <= pd.to_datetime(end_date)) & 
    (data['weathersit'].isin(weather_options))
]

# Main dashboard
st.title('Bike Sharing Dashboard')

# Show filtered data
st.write(f"Showing data from {start_date} to {end_date}")
st.dataframe(filtered_data)

# Visualize Total Users (cnt) over time
st.subheader('Total Users Over Time')
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered_data['dteday'], filtered_data['cnt'], color='blue', label='Total Users')
ax.set_xlabel('Date')
ax.set_ylabel('Total Users')
ax.set_title('Total Users Over Time')
ax.grid(True)
st.pyplot(fig)

# Visualize correlation between 'cnt' and 'weathersit'
st.subheader('Correlation between Total Users and Weather Conditions')
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(filtered_data['weathersit'], filtered_data['cnt'], alpha=0.5, color='purple')
ax.set_xlabel('Weather Situation (1: Clear, 2: Mist, 3: Light Snow/Rain)')
ax.set_ylabel('Total Users')
ax.set_title('Correlation between Total Users and Weather Conditions')
ax.grid(True)
st.pyplot(fig)

# Additional statistics
st.subheader('Additional Statistics')
st.write(f"Average number of total users: {filtered_data['cnt'].mean():.2f}")
st.write(f"Max number of total users: {filtered_data['cnt'].max()}")
st.write(f"Min number of total users: {filtered_data['cnt'].min()}")
