import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv('EDA_Gold_Silver_prices.csv')

# Set page configuration
st.set_page_config(page_title='Gold and Silver Prices EDA', layout='wide')

# Display the dataset and summary statistics
st.title('Gold and Silver Prices in Indian Currency')
st.header('Analysis for Applied Materials - By Tanmay Ghosh')
st.dataframe(data)

st.subheader('Summary Statistics')
st.write(data.describe())

# Perform exploratory data analysis
st.header('Exploratory Data Analysis')

# Line chart for gold prices
st.subheader('Gold Prices')
st.line_chart(data['GoldPrice'])

# Line chart for silver prices
st.subheader('Silver Prices')
st.line_chart(data['SilverPrice'])

# Histogram for gold prices
st.subheader('Gold Prices Distribution')
plt.hist(data['GoldPrice'], bins='auto')
st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)

# Histogram for silver prices
st.subheader('Silver Prices Distribution')
plt.hist(data['SilverPrice'], bins='auto')
st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)

# Data filtering
st.header('Data Filtering')

# Filtering options
price_range = st.slider('Select Price Range', min_value=data['GoldPrice'].min(),
                        max_value=data['GoldPrice'].max(), value=(data['GoldPrice'].min(), data['GoldPrice'].max()))

filtered_data = data[(data['GoldPrice'].between(price_range[0], price_range[1]))]

# Display filtered data
st.subheader('Filtered Data')
st.write(filtered_data)

if st.button('Group by Month'):
    data['Month'] = pd.to_datetime(data['Month'], errors='coerce').dt.month  # Extract month from date
    grouped_data = data.groupby('Month').mean()
    st.subheader('Grouped Data by Month - prices in each month across years averages')
    st.write(grouped_data)
    
if st.button('Correlation Matrix'):
        data['Month'] = pd.to_datetime(data['Month'], errors='coerce').dt.month
        grouped_data = data.groupby('Month').mean()
        correlation_matrix = grouped_data[['GoldPrice', 'SilverPrice']].corr()
        st.subheader('Correlation Matrix')
        st.write(correlation_matrix)