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
st.markdown('#### Assumption - Data provided are prices for per 31.8 grams')
st.markdown('#### PER TROY OUNCE ANALYSIS BELOW - 31.8 grams')
col1, col2 = st.columns(2)
with col1:
    st.write("Per Troy Ounce Data")
    st.write(data_view)

with col2:
    st.write("Describe data")
    st.dataframe(data.describe().round(2))

# Perform exploratory data analysis
st.header('Exploratory Data Analysis')

# Line chart for gold prices
st.subheader('Gold Prices in INR (Y) per day (X) per Troy ounce')
st.line_chart(data['GoldPrice'])


# Line chart for silver prices
st.subheader('Silver Prices in INR (Y) per day (X) per troy ounce')
st.line_chart(data['SilverPrice'])

# Data filtering
st.header('Data Filtering')

# Filtering options
price_range = st.slider('Select Price Range', 
                        min_value=float(data['GoldPrice'].min()),
                        max_value=float(data['GoldPrice'].max()), 
                        value=(float(data['GoldPrice'].min()), float(data['GoldPrice'].max())))

filtered_data = data[(data['GoldPrice'].between(price_range[0], price_range[1]))]
desc_fil_data = filtered_data.describe()

# Display filtered data
st.subheader('Filtered Data')
col1, col2 = st.columns(2)
with col1:
    st.write("Filtered Data")
    st.write(filtered_data)

with col2:
    st.write("Describe data")
    st.dataframe(desc_fil_data)

if st.button('Group by Month'):
    data['Month'] = pd.to_datetime(data['Month'], errors='coerce').dt.month  # Extract month from date
    grouped_data = data.groupby('Month')['GoldPrice', 'SilverPrice'].mean().round(0).reset_index()
    grouped_data['Month'] = grouped_data['Month'].round(0).astype(str)
    Month_Name = []
    for i in range(grouped_data.shape[0]):
        month_num = grouped_data['Month'][i]
        if month_num == '1':
            res = 'January'
        elif month_num == '2':
            res = 'February'
        elif month_num == '3':
            res = 'March'
        elif month_num == '4':
            res = 'April'
        elif month_num == '5':
            res = 'May'
        elif month_num == '6':
            res = 'June'
        elif month_num == '7':
            res = 'July'
        elif month_num == '8':
            res = 'August'
        elif month_num == '9':
            res = 'September'
        elif month_num == '10':
            res = 'October'
        elif month_num == '11':
            res = 'November'
        elif month_num == '12':
            res = 'December'
        else:
            res = 'Unknown'
        Month_Name.append(res)

    grouped_data['Month_Name'] = Month_Name
    st.markdown('##### Top Gold and Silver Prices months (Per Troy Ounce)')
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Top 5 Months of Gold Price per KG
    top_5_month_gold = grouped_data.nlargest(5, 'GoldPrice')
    sns.barplot(data=top_5_month_gold, x='Month_Name', y='GoldPrice', ax=axes[0])
    axes[0].set_title('Top 5 Months of Gold Price Per Troy Ounce')
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel('Gold Price')

    # Top 5 Months of Silver Price per KG
    top_5_month_silver = grouped_data.nsmallest(5, 'SilverPrice')
    sns.barplot(data=top_5_month_silver, x='Month_Name', y='SilverPrice', ax=axes[1])
    axes[1].set_title('Top 5 Months of Silver Price per Troy Ounce')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Silver Price')
    plt.tight_layout()
    st.pyplot(fig)

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

## PER KILO ANALYSIS
st.header('Analysis for Per Kilo price for gold and silver')
data_kg = pd.read_csv('EDA_Gold_Silver_prices.csv')
data_kg['Month'] = pd.to_datetime(data_kg['Month'], errors='coerce').dt.month
data_kg[['SilverPrice','GoldPrice']] = data_kg[['SilverPrice','GoldPrice']].apply(lambda x :(1000/31.8)* x, axis=1)
data_kg_view = data_kg.copy()
data_kg_view['SilverPrice'] = data_kg_view['SilverPrice'].round(2).astype(str) + ' INR'
data_kg_view['GoldPrice'] = data_kg_view['GoldPrice'].round(2).astype(str) + ' INR'
st.dataframe(data_kg_view)



if st.button('Group by Month (Per Kilo)'):
    grouped_data = data_kg.groupby('Month')['GoldPrice', 'SilverPrice'].mean().round(0).reset_index()
    grouped_data['Month'] = grouped_data['Month'].round(0).astype(str)
    Month_Name = []
    for i in range(grouped_data.shape[0]):
        month_num = grouped_data['Month'][i]
        if month_num == '1':
            res = 'January'
        elif month_num == '2':
            res = 'February'
        elif month_num == '3':
            res = 'March'
        elif month_num == '4':
            res = 'April'
        elif month_num == '5':
            res = 'May'
        elif month_num == '6':
            res = 'June'
        elif month_num == '7':
            res = 'July'
        elif month_num == '8':
            res = 'August'
        elif month_num == '9':
            res = 'September'
        elif month_num == '10':
            res = 'October'
        elif month_num == '11':
            res = 'November'
        elif month_num == '12':
            res = 'December'
        else:
            res = 'Unknown'
        Month_Name.append(res)

    grouped_data['Month_Name'] = Month_Name
    st.dataframe(grouped_data)
    st.markdown('##### Top Gold and Silver Prices months (Per KG)')
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Top 5 Months of Gold Price per KG
    top_5_month_gold = grouped_data.nlargest(5, 'GoldPrice')
    sns.barplot(data=top_5_month_gold, x='Month_Name', y='GoldPrice', ax=axes[0])
    axes[0].set_title('Top 5 Months of Gold Price Pwr KG')
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel('Gold Price')

    # Top 5 Months of Silver Price per KG
    top_5_month_silver = grouped_data.nsmallest(5, 'SilverPrice')
    sns.barplot(data=top_5_month_silver, x='Month_Name', y='SilverPrice', ax=axes[1])
    axes[1].set_title('Top 5 Months of Silver Price per KG')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Silver Price')
    plt.tight_layout()
    st.pyplot(fig)

    
if st.button('Correlation Matrix Per Kilo'):
        data_kg['Month'] = pd.to_datetime(data['Month'], errors='coerce').dt.month
        grouped_data = data_kg.groupby('Month').mean()
        correlation_matrix = grouped_data[['GoldPrice', 'SilverPrice']].corr()
        st.subheader('Correlation Matrix per Kilo')
        st.write(correlation_matrix)

