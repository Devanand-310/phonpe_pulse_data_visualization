import streamlit as st
from sqlalchemy import create_engine
import base64
import pandas as pd
import plotly.express as px
import requests
import json

st.set_page_config(layout="wide")
# Database connection
connection = create_engine('mysql+pymysql://root:Janu19042002@localhost/phonepe')
image_path = 'images/phonepe.png'

# Function to encode image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image(image_path)

# Custom CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #00000;
    }}
    .title {{
        display: flex;
        align-items: center;
        color: white;
        font-size: 50px;
        margin-top: 20px;
        margin-left: 2px;
        justify-content: flex-start;
    }}
    .title img {{
        width: 50px;
        margin-right: 10px;
        border-radius: 15px;
    }}
    .container {{
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-left: 20px;
    }}
    .button-container {{
        display: flex;
        justify-content: flex-start;
        gap: 10px;
        margin-bottom: 20px;
        margin-left: 20px;
    }}
    .stButton>button {{
        background-color: #4CAF50; /* Green background */
        border: 2px solid #4CAF50; /* Green border */
        color: white; /* White text */
        padding: 10px 60px; /* Padding */
        text-align: center; /* Centered text */
        text-decoration: none; /* No underline */
        display: inline-block; /* Inline-block */
        font-size: 16px; /* Font size */
        cursor: pointer; /* Pointer/hand icon */
        border-radius: 8px; /* Rounded corners */
        flex: 1; /* Equal width */
        width: 500px; /* Fixed width */
        height: 50px; /* Fixed height */
    }}
    .stButton>button:hover {{
        background-color: white; /* White background on hover */
        color: #4CAF50; /* Green text on hover */
        border: 2px solid #4CAF50; /* Green border on hover */
    }}

    </style>
    <h1 class='title'>
        <img src="data:image/png;base64,{image_base64}" alt="Logo"> PhonePe Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .plotly-hoverlayer .hovertext {
        animation: hover-animation 0.5s forwards;
    }

    @keyframes hover-animation {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
        }
        100% {
            transform: scale(1);
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to fetch state data
def fetch_state_data(connection, state):
    query = f"""
    SELECT Year, SUM(Transaction_amount) AS Transaction_amount
    FROM phonepe.agg_transaction
    WHERE State = '{state}'
    GROUP BY Year
    """
    return pd.read_sql(query, connection)

# Function to fetch aggregate data
def fetch_agg_data(engine):
    query = """
    SELECT State, SUM(Transaction_amount) AS Transaction_amount
    FROM phonepe.agg_transaction
    GROUP BY State
    """
    return pd.read_sql(query, engine)

# Define button labels
button_labels = ["Home", "User Detail", "Transaction", "About"]

# Create buttons and handle clicks using session state
with st.container():
    cols = st.columns(len(button_labels))
    for col, label in zip(cols, button_labels):
        if col.button(label):
            st.session_state['button_clicked'] = label
geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
# Display chart if 'Home' button is clicked
if st.session_state.get('button_clicked') == 'Home':
    
    data = fetch_agg_data(connection)
    data_reset = data.reset_index(drop=True)
    
    fig_choropleth = px.choropleth(
        data,
        geojson=geojson_url,
        featureidkey='properties.ST_NM',
        locations='State',
        color='Transaction_amount',
        hover_name='State',
        color_continuous_scale='turbo',
        title='Total Transaction Amount by State',
        labels={'Transaction_amount': 'Transaction Amount'}
    )
    
    fig_choropleth.update_geos(fitbounds="locations", visible=False)
    fig_choropleth.update_layout(
        plot_bgcolor='#000000',  
        paper_bgcolor='#000000' , 
        height=800,
        width=6000
    )
    fig_choropleth.update_traces(
        hovertemplate='<b>%{location}</b><br>Transaction Amount: %{z}<extra></extra>',
        marker=dict(line=dict(width=1))
    )
    st.plotly_chart(fig_choropleth)
    
    state_selected = st.selectbox("Select a state to view details", options=data_reset['State'].unique())
    
    if state_selected:
        state_data = fetch_state_data(connection, state_selected)
        col1, col2 = st.columns(2)
        
        with col1:
            
            fig = px.bar(
                    state_data.reset_index(), 
                    x='Year', 
                    y='Transaction_amount', 
                    title=f'Transaction Amount of {state_selected}',
                    color='Transaction_amount',
                    color_discrete_sequence=px.colors.qualitative.D3
            )
            st.plotly_chart(fig)
            
        
        with col2:
            fig_line = px.line(
                state_data,
                x='Year',
                y='Transaction_amount',
                title=f'Total Transaction Amount by Year for {state_selected}',
                labels={'Transaction_amount': 'Transaction Amount'}
            )
            st.plotly_chart(fig_line)

def fetch_user(connection):
    query ="""select SUM(User_Percentage) AS User_percentage,User_Brand,Year
        from phonepe.agg_users
         GROUP BY  User_Brand,Year
    """
    return pd.read_sql(query, connection)

def fetch_user_state(connection, state):
    query = f"""
    SELECT User_Brand, SUM(User_Percentage) AS User_percentage
    FROM phonepe.agg_users
    WHERE State = '{state}'
    GROUP BY User_Brand
    """
    return pd.read_sql(query, connection)

if st.session_state.get('button_clicked') == 'User Detail':
    data = fetch_user(connection)
    fig = px.bar(
        data,
        x='User_Brand',
        y='User_percentage',
        color='User_Brand',
        animation_frame='Year',
        title='PhonePe Users By Smartphone',
        labels={'User_Brand': 'User Brand', 'User_percentage': 'User Percentage'},
        color_discrete_sequence=px.colors.qualitative.Plotly  # Change to any color sequence you prefer
    )
    st.plotly_chart(fig)
    st.title("Smartphone Users Based on State")
    

    data = fetch_agg_data(connection)
    data_reset = data.reset_index(drop=True)

    state_selected = st.selectbox("Select a state to view details", options=data_reset['State'].unique())
    
    if state_selected:
        state_data = fetch_user_state(connection,state_selected)
        col1,col2 = st.columns(2)
        
        with col1:
            fig_pie = px.pie(
                state_data,
                names='User_Brand',
                values='User_percentage',
                color='User_Brand',
                title=f'PhonePe Users By Smartphone in {state_selected}',
                labels={'User_Brand': 'User Brand', 'User_percentage': 'User Percentage'}
            )
            st.plotly_chart(fig_pie)

        with col2:
            df3 = fetch_user(connection)
            data_grouped = df3.groupby(['Year', 'User_Brand'])['User_percentage'].sum().reset_index()

            # Create stacked bar plot with Plotly Express
            fig_stacked_bar = px.bar(
                data_grouped,
                x='Year',
                y='User_percentage',
                color='User_Brand',
                title='Stacked Bar Plot',
                labels={'User_percentage': 'Total Value', 'Year': 'Year'},
                barmode='stack',  # Set barmode to 'stack' for stacked bar plot
                height=500  # Adjust height as needed
            )

            st.plotly_chart(fig_stacked_bar)

def fetch_trans_type(connection,state):
    query = f"""SELECT Transaction_type, State, Year, SUM(Transaction_count) AS Transaction_count
            from phonepe.agg_transaction
            where State = '{state}'
            GROUP BY  Transaction_type, State, Year"""
    return pd.read_sql(query, connection)

def fetch_district_details(connection,state):
    query = f"""SELECT SUM(top_trans.Transaction_amount) AS Transaction_amount, 
    top_trans.Pincodes, 
    SUM(top_trans.Transaction_count) AS Transaction_counts,
    pincode.District
    FROM top_trans 
    JOIN pincode ON top_trans.Pincodes = pincode.Pincode 
    WHERE top_trans.State = '{state}'
    GROUP BY top_trans.Pincodes, pincode.District
    ORDER BY Transaction_amount DESC
    LIMIT 10;"""
    return pd.read_sql(query, connection)     

if st.session_state.get('button_clicked') == 'Transaction':
    data = fetch_agg_data(connection)
    data_reset = data.reset_index(drop=True)

    state_selected = st.selectbox("Select a state to view details", options=data_reset['State'].unique())
    df3 = fetch_trans_type(connection,state_selected)
    data_grouped = df3.groupby(['Year','Transaction_type'])['Transaction_count'].sum().reset_index()

    fig_stacked_bar = px.bar(
                data_grouped,
                x='Year',
                y='Transaction_count',
                color='Transaction_type',
                title=f'Most commonly used transaction type in {state_selected}',
                labels={'Transaction_count': 'Total Value', 'Year': 'Year'},
                barmode='stack',  # Set barmode to 'stack' for stacked bar plot
                height=500  # Adjust height as needed
            )

    st.plotly_chart(fig_stacked_bar)
    st.title(f'{state_selected} District based Visualization')    
    col1,col2 = st.columns(2)
    with col1:
        data_frame = fetch_district_details(connection,state_selected)
        st.dataframe(data_frame)

    with col2:
        query = f"""SELECT DISTINCT SUM(top_users.Registered_users) AS Total_users, 
        top_users.Pincode, 
        pincode.District
        FROM top_users 
        JOIN pincode ON top_users.Pincode = pincode.Pincode 
        WHERE top_users.State = '{state_selected}'
        GROUP BY top_users.Pincode, pincode.District
        ORDER BY Total_users DESC
        LIMIT 10;"""
        data_user = pd.read_sql(query,connection)
        st.dataframe(data_user)

st.markdown(
    """
    <style>
    .custom-text {
        font-family: 'Arial', sans-serif;
        color: #4A90E2;
        font-size: 20px;
        font-weight: bold;
        animation: fadeIn 2s ease-in-out;
    }

    @keyframes fadeIn {
        0% {opacity: 0;}
        100% {opacity: 1;}
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.session_state.get('button_clicked') == 'About':
    st.markdown(
        """
        <p class="custom-text">PhonePe is an Indian digital payments and financial technology company founded in December 2015 by Sameer Nigam, Rahul Chari, and Burzin Engineer. As a subsidiary of Flipkart, PhonePe has grown to become one of India's leading digital payment platforms, leveraging the Unified Payments Interface (UPI) system. It offers a range of services including money transfers, utility bill payments, mobile recharges, online shopping, and investment options like mutual funds and insurance.</p>
        
        <p class="custom-text">PhonePe's growth trajectory has been remarkable. By providing a user-friendly interface and a wide array of services, it quickly gained a large user base. It became the first UPI-based app to surpass 10 million app downloads and continues to expand its user base, boasting over 350 million registered users and facilitating billions of transactions monthly.</p>
        
        <p class="custom-text">The company's strategic partnerships and constant innovation have been pivotal in its growth. It collaborates with numerous merchants and service providers, enhancing its ecosystem. Additionally, PhonePe has expanded its footprint into financial services, including insurance and mutual fund investments, diversifying its revenue streams.</p>
        
        <p class="custom-text">PhonePe's commitment to secure, reliable, and seamless transactions has solidified its position in the competitive digital payments market, contributing significantly to the digitalization of India's economy. As it continues to innovate and expand, PhonePe is poised to play a crucial role in shaping the future of digital payments in India.</p>
        """,
        unsafe_allow_html=True
    )