import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
data = pd.read_csv('EDA_Gold_Silver_prices.csv')
data_view = data[['SilverPrice','GoldPrice']]
data_view['SilverPrice'] = data_view['SilverPrice'].round(2).astype(str) + ' INR'
data_view['GoldPrice'] = data_view['GoldPrice'].round(2).astype(str) + ' INR'


# Set page configuration
st.set_page_config(page_title='Gold and Silver Prices EDA', layout='wide')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Display the dataset and summary statistics
st.title('Gold and Silver Prices in Indian Currency')
st.header('Analysis for Applied Materials - By Tanmay Ghosh')
st.dataframe(data_view)

st.subheader('Summary Statistics')
st.write(data.describe().round(2))

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
price_range = st.slider('Select Price Range', 
                        min_value=float(data['GoldPrice'].min()),
                        max_value=float(data['GoldPrice'].max()), 
                        value=(float(data['GoldPrice'].min()), float(data['GoldPrice'].max())))

filtered_data = data[(data['GoldPrice'].between(price_range[0], price_range[1]))]

# Display filtered data
st.subheader('Filtered Data')
st.write(filtered_data)

if st.button('Group by Month'):
    data['Month'] = pd.to_datetime(data['Month'], errors='coerce').dt.month  # Extract month from date
    grouped_data = data.groupby('Month')['GoldPrice', 'SilverPrice'].mean().round(0).reset_index()
    grouped_data['Month'] = grouped_data['Month'].round(0).astype(str)
    data['Month'] = pd.to_datetime(data['Month'], errors='coerce').dt.month  # Extract month from date
    Month_Name = []
    for i in range(grouped_data.shape[0]):
        month_num = grouped_data['Month'][i]
        if month_num == '1.0':
            res = 'January'
        elif month_num == '2.0':
            res = 'February'
        elif month_num == '3.0':
            res = 'March'
        elif month_num == '4.0':
            res = 'April'
        elif month_num == '5.0':
            res = 'May'
        elif month_num == '6.0':
            res = 'June'
        elif month_num == '7.0':
            res = 'July'
        elif month_num == '8.0':
            res = 'August'
        elif month_num == '9.0':
            res = 'September'
        elif month_num == '10.0':
            res = 'October'
        elif month_num == '11.0':
            res = 'November'
        elif month_num == '12.0':
            res = 'December'
        else:
            res = 'Unknown'
        Month_Name.append(res)

    grouped_data['Month_Name'] = Month_Name
    # Top 5 brands by profit
    top_5_month_gold = grouped_data.nlargest(5, 'GoldPrice')
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_5_month_gold, x='Month_Name', y='GoldPrice')
    plt.title('Top 5 Months of Gold Price')
    plt.xlabel('Month')
    plt.ylabel('Gold Price')
    st.pyplot()

    # Bottom 5 brands by profit
    top_5_month_silver = grouped_data.nsmallest(5, 'SilverPrice')
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_5_month_silver, x='Month_Name', y='SilverPrice')
    plt.title('Top 5 Months Silver Price')
    plt.xlabel('Month')
    plt.ylabel('Silver Price')
    st.pyplot()

    grouped_data['SilverPrice'] = grouped_data['SilverPrice'].astype(str) + ' INR'
    grouped_data['GoldPrice'] = grouped_data['GoldPrice'].astype(str) + ' INR'
    st.subheader('Grouped Data by Month - prices in each month across years averages')
    st.write(grouped_data)   
if st.button('Correlation Matrix'):
        data['Month'] = pd.to_datetime(data['Month'], errors='coerce').dt.month
        grouped_data = data.groupby('Month').mean()
        correlation_matrix = grouped_data[['GoldPrice', 'SilverPrice']].corr()
        st.subheader('Correlation Matrix')
        st.write(correlation_matrix)
