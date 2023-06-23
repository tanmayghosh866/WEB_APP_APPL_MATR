%pip install matplotlib
%pip install streamlit
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date

# Read the data from the Excel file
df_total = pd.read_csv('currencies.csv')
df_min = df_total[['ID','Date','Day','Euro','Japanese Yen','U.K. Pound Sterling','U.S. Dollar','Chinese Yuan','Australian Dollar','Indian Rupee']]
df_min.to_excel('df.xlsx', index=False)
global df
df = pd.read_excel('df.xlsx')
df['Date'] = pd.to_datetime(df['Date']).dt.date

# Function to update the data in the DataFrame
def update_excel():
    df.to_excel('df.xlsx', index=False)
    st.success('Data Updated Successfully!')

# Function to delete a row from the DataFrame
def delete_row(row):
    global df
    df.drop(row, inplace=True)
    df.to_excel('df.xlsx', index=False)
    st.success('Row Deleted Successfully!')

# Function to modify a row in the DataFrame
def modify_row(row, values):
    df = pd.read_excel('df.xlsx')
    df.at[row, 'Euro'] = values['Euro']
    df.at[row, 'Japanese Yen'] = values['Japanese Yen']
    df.at[row, 'U.K. Pound Sterling'] = values['U.K. Pound Sterling']
    df.at[row, 'U.S. Dollar'] = values['U.S. Dollar']
    df.at[row, 'Chinese Yuan'] = values['Chinese Yuan']
    df.at[row, 'Australian Dollar'] = values['Australian Dollar']
    df.at[row, 'Indian Rupee'] = values['Indian Rupee']
    update_excel()

# Function to add a new row to the DataFrame
def add_row(values):
    df = pd.read_excel('df.xlsx')
    new_id = df['ID'].max() + 1
    new_row = {
        'ID': new_id,
        'Euro': values['Euro'],
        'Japanese Yen': values['Japanese Yen'],
        'U.K. Pound Sterling': values['U.K. Pound Sterling'],
        'U.S. Dollar': values['U.S. Dollar'],
        'Chinese Yuan': values['Chinese Yuan'],
        'Australian Dollar': values['Australian Dollar'],
        'Indian Rupee': values['Indian Rupee'],
    }
    df = df.append(new_row, ignore_index=True)
    update_excel()

# Streamlit layout
st.title('Currency Analysis For Applied Materials')
st.header('By Tanmay Ghosh')

row_input = st.text_input('Select Row (ID)', value='', key='row_input', type='default')
st.markdown('#### Search rows from the Database')
search_button = st.button('Search')

if search_button:
    df = pd.read_excel('df.xlsx')
    try:
        row_id = int(row_input)
        if row_id in df['ID'].values:
            row = df[df['ID'] == row_id]
            values = {
                'Euro': row['Euro'].values[0],
                'Japanese Yen': row['Japanese Yen'].values[0],
                'U.K. Pound Sterling': row['U.K. Pound Sterling'].values[0],
                'U.S. Dollar': row['U.S. Dollar'].values[0],
                'Chinese Yuan': row['Chinese Yuan'].values[0],
                'Australian Dollar': row['Australian Dollar'].values[0],
                'Indian Rupee': row['Indian Rupee'].values[0],
            }
            st.text_input('Euro:', value=values['Euro'], key='Euro')
            st.text_input('Japanese Yen:', value=values['Japanese Yen'], key='Japanese Yen')
            st.text_input('U.K. Pound Sterling:', value=values['U.K. Pound Sterling'], key='U.K. Pound Sterling')
            st.text_input('U.S. Dollar:', value=values['U.S. Dollar'], key='U.S. Dollar')
            st.text_input('Chinese Yuan:', value=values['Chinese Yuan'], key='Chinese Yuan')
            st.text_input('Australian Dollar:', value=values['Australian Dollar'], key='Australian Dollar')
            st.text_input('Indian Rupee:', value=values['Indian Rupee'], key='Indian Rupee')
        else:
            st.error('ID not found!')
    except ValueError:
        st.error('Invalid row ID. Please enter a valid integer.')
        
st.markdown('#### Search and then Modify rows from the Database')
modify_button = st.button('Modify')

if modify_button:
    df = pd.read_excel('df.xlsx')
    try:
        row_id = int(row_input)
        if row_id in df['ID'].values:
            row = df[df['ID'] == row_id]
            values = {
                'Euro': st.text_input('Euro:', value=row['Euro'].values[0], key='Euro_modify'),
                'Japanese Yen': st.text_input('Japanese Yen:', value=row['Japanese Yen'].values[0], key='Japanese Yen_modify'),
                'U.K. Pound Sterling': st.text_input('U.K. Pound Sterling:', value=row['U.K. Pound Sterling'].values[0], key='U.K. Pound Sterling_modify'),
                'U.S. Dollar': st.text_input('U.S. Dollar:', value=row['U.S. Dollar'].values[0], key='U.S. Dollar_modify'),
                'Chinese Yuan': st.text_input('Chinese Yuan:', value=row['Chinese Yuan'].values[0], key='Chinese Yuan_modify'),
                'Australian Dollar': st.text_input('Australian Dollar:', value=row['Australian Dollar'].values[0], key='Australian Dollar_modify'),
                'Indian Rupee': st.text_input('Indian Rupee:', value=row['Indian Rupee'].values[0], key='Indian Rupee_modify'),
            }
            modify_row(row_id, values)
        else:
            st.error('ID not found!')
    except ValueError:
        st.error('Invalid row ID. Please enter a valid integer.')
st.markdown('### Add new rows to the Database')
add_button = st.button('Add row form')
euro = st.text_input('Euro:', value='', key='Euro_add')
jpy = st.text_input('Japanese Yen:', value='', key='Japanese Yen_add')
uk = st.text_input('U.K. Pound Sterling:', value='', key='U.K. Pound Sterling_add')
cny = st.text_input('Chinese Yuan:', value='', key='Chinese Yuan_add')
usd = st.text_input('U.S. Dollar:', value='', key='U.S. Dollar_add')
aud = st.text_input('Australian Dollar:', value='', key='Australian Dollar_add')
inr = st.text_input('Indian Rupee:', value='', key='Indian Rupee_add')
if add_button:
    if euro != '' and jpy != '' and uk != '' and usd != '' and cny != '' and aud != '' and inr != '':
        values = {
            'Euro': euro,
            'Japanese Yen': jpy,
            'U.K. Pound Sterling': uk,
            'U.S. Dollar': usd,
            'Chinese Yuan': cny,
            'Australian Dollar': aud,
            'Indian Rupee': inr,
        }
        add_row(values)
        st.success('Row Added Successfully!')
    else:
        st.warning('Please provide values for all inputs before adding the row.')

st.markdown('#### Convert and view wide data to long format')
convert_button = st.button('Convert to Long')

if convert_button:
    df_long = pd.melt(df, id_vars='Date', value_vars=['Euro', 'Japanese Yen', 'U.K. Pound Sterling', 'U.S. Dollar', 'Chinese Yuan', 'Australian Dollar', 'Indian Rupee'], var_name='Currency', value_name='Rate')
    st.dataframe(df_long)

st.markdown('#### Describe the Data')
st.markdown('##### Select Currency')
currency_names = ['Euro', 'Japanese Yen', 'U.K. Pound Sterling', 'U.S. Dollar', 'Chinese Yuan', 'Australian Dollar', 'Indian Rupee']
currency_filter = st.selectbox('Select Currency', currency_names)
Statistics = st.button('Statistics')
if Statistics:
    df = pd.read_excel('df.xlsx')
    if currency_filter == 'Euro':
            df_long = pd.melt(df, id_vars='Day', value_vars=['Euro'], var_name='Currency', value_name='Rate')
            description = df_long.describe()
            st.dataframe(description)
    elif currency_filter == 'Japanese Yen':
            df_long = pd.melt(df, id_vars='Day', value_vars=['Japanese Yen'], var_name='Currency', value_name='Rate')
            description = df_long.describe()
            st.dataframe(description)
    elif currency_filter == 'U.K. Pound Sterling':
            df_long = pd.melt(df, id_vars='Day', value_vars=['U.K. Pound Sterling'], var_name='Currency', value_name='Rate')
            description = df_long.describe()
            st.dataframe(description)
    elif currency_filter == 'U.S. Dollar':
            df_long = pd.melt(df, id_vars='Day', value_vars=['U.S. Dollar'], var_name='Currency', value_name='Rate')
            description = df_long.describe()
            st.dataframe(description)
    elif currency_filter == 'Chinese Yuan':
            df_long = pd.melt(df, id_vars='Day', value_vars=['Chinese Yuan'], var_name='Currency', value_name='Rate')
            description = df_long.describe()
            st.dataframe(description)
    elif currency_filter == 'Australian Dollar':
            df_long = pd.melt(df, id_vars='Day', value_vars=['Australian Dollar'], var_name='Currency', value_name='Rate')
            description = df_long.describe()
            st.dataframe(description)
    elif currency_filter == 'Indian Rupee':
            df_long = pd.melt(df, id_vars='Day', value_vars=['Indian Rupee'], var_name='Currency', value_name='Rate')
            description = df_long.describe()
            st.dataframe(description)
    else:
          pass


st.markdown('#### View graphs on Currency analysis')
st.markdown('##### Select Currency')
Show_Graph = st.button('Show Graph')
if Show_Graph:
    df = pd.read_excel('df.xlsx')
    if currency_filter == 'Euro':
            df_long = pd.melt(df, id_vars='Day', value_vars=['Euro'], var_name='Currency', value_name='Rate')
            fig, ax = plt.subplots()
            filtered_data = df_long[df_long['Currency'] == currency_filter]
            ax.plot(filtered_data['Day'], filtered_data['Rate'])
            ax.set_xlabel('Day')
            ax.set_ylabel('Rate')
            st.pyplot(fig)
    elif currency_filter == 'Japanese Yen':
            df_long = pd.melt(df, id_vars='Day', value_vars=['Japanese Yen'], var_name='Currency', value_name='Rate')
            fig, ax = plt.subplots()
            filtered_data = df_long[df_long['Currency'] == currency_filter]
            ax.plot(filtered_data['Day'], filtered_data['Rate'])
            ax.set_xlabel('Day')
            ax.set_ylabel('Rate')
            st.pyplot(fig)
    elif currency_filter == 'U.K. Pound Sterling':
            df_long = pd.melt(df, id_vars='Day', value_vars=['U.K. Pound Sterling'], var_name='Currency', value_name='Rate')
            fig, ax = plt.subplots()
            filtered_data = df_long[df_long['Currency'] == currency_filter]
            ax.plot(filtered_data['Day'], filtered_data['Rate'])
            ax.set_xlabel('Day')
            ax.set_ylabel('Rate')
            st.pyplot(fig)
    elif currency_filter == 'U.S. Dollar':
            df_long = pd.melt(df, id_vars='Day', value_vars=['U.S. Dollar'], var_name='Currency', value_name='Rate')
            fig, ax = plt.subplots()
            filtered_data = df_long[df_long['Currency'] == currency_filter]
            ax.plot(filtered_data['Day'], filtered_data['Rate'])
            ax.set_xlabel('Day')
            ax.set_ylabel('Rate')
            st.pyplot(fig, show_spinner=False)
    elif currency_filter == 'Chinese Yuan':
            df_long = pd.melt(df, id_vars='Day', value_vars=['Chinese Yuan'], var_name='Currency', value_name='Rate')
            fig, ax = plt.subplots()
            filtered_data = df_long[df_long['Currency'] == currency_filter]
            ax.plot(filtered_data['Day'], filtered_data['Rate'])
            ax.set_xlabel('Day')
            ax.set_ylabel('Rate')
            st.pyplot(fig)
    elif currency_filter == 'Australian Dollar':
            df_long = pd.melt(df, id_vars='Day', value_vars=['Australian Dollar'], var_name='Currency', value_name='Rate')
            fig, ax = plt.subplots()
            filtered_data = df_long[df_long['Currency'] == currency_filter]
            ax.plot(filtered_data['Day'], filtered_data['Rate'])
            ax.set_xlabel('Day')
            ax.set_ylabel('Rate')
            st.pyplot(fig)
    elif currency_filter == 'Indian Rupee':
            df_long = pd.melt(df, id_vars='Day', value_vars=['Indian Rupee'], var_name='Currency', value_name='Rate')
            fig, ax = plt.subplots()
            filtered_data = df_long[df_long['Currency'] == currency_filter]
            ax.plot(filtered_data['Day'], filtered_data['Rate'])
            ax.set_xlabel('Day')
            ax.set_ylabel('Rate')
            st.pyplot(fig)
    else:
            pass
