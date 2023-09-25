# import the modules
import os
import subprocess
import json
import io
import xlsxwriter
import pandas as pd
import mysql.connector
import sqlite3
from sqlalchemy import create_engine
import datetime as dt
import streamlit as st
from streamlit_option_menu import option_menu
import PIL 
from PIL import Image
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.add_vertical_space import add_vertical_space



# set the page configuration
st.set_page_config(
                    page_title = 'PhonePe Data Visualization', layout = 'wide',
                    page_icon = "Images/image_phonepe.webp"
                    )

#Dataframe of aggregated Transaction
path_agg_tran = r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/pulse-master/data/aggregated/transaction/country/india/state/"
Agg_tran_list=os.listdir(path_agg_tran)

clm={'State':[], 'Year':[],'Quater':[],'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}
for i in Agg_tran_list:
    p_i=path_agg_tran+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['transactionData']:
                Name=z['name']
                count=z['paymentInstruments'][0]['count']
                amount=z['paymentInstruments'][0]['amount']
                clm['Transaction_type'].append(Name)
                clm['Transaction_count'].append(count)
                clm['Transaction_amount'].append(amount)
                clm['State'].append(i)
                clm['Year'].append(j)
                clm['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
Agg_Trans=pd.DataFrame(clm)


#Dataframe for aggregated user
path_agg_user = r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/pulse-master/data/aggregated/user/country/india/state/"
Agg_user_list=os.listdir(path_agg_user)


clm={'State':[], 'Year':[],'Quater':[],'User_Brand':[], 'User_Count':[], 'User_Percentage':[]}
for i in Agg_user_list:
    p_i=path_agg_user+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            #print(D)
            for z in D['data']['usersByDevice'] or []:
                if None:
                    pass
                else:
                    Brand=z['brand'] 
                    count=z['count'] 
                    percentage=z['percentage']
                    clm['User_Brand'].append(Brand)
                    clm['User_Count'].append(count)
                    clm['User_Percentage'].append(percentage)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
                
#Succesfully created a dataframe
Agg_Users=pd.DataFrame(clm)


#Dataframe for Map Transaction
path_map_tran = r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/pulse-master/data/map/transaction/hover/country/india/state/"
map_tran_list=os.listdir(path_map_tran)

clm={'State':[], 'Year':[],'Quater':[],'District_Name':[], 'Distict_Transaction_count':[], 'District_Transaction_amount':[]}
for i in map_tran_list:
    p_i=path_map_tran+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['hoverDataList']:
              Name=z['name']
              count=z['metric'][0]['count']
              amount=z['metric'][0]['amount']
              clm['District_Name'].append(Name)
              clm['Distict_Transaction_count'].append(count)
              clm['District_Transaction_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
Map_Trans=pd.DataFrame(clm)


#Dataframe for Map user
path_map_user = r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/pulse-master/data/map/user/hover/country/india/state/"
Map_user_list=os.listdir(path_map_user)


clm={'State':[], 'Year':[],'Quater':[],'District':[], 'Registered_users':[]}
for i in Map_user_list:
    p_i=path_map_user+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            #print(D)
            for z in D['data']['hoverData'].items():
                    dist=z[0] 
                    count=z[1]['registeredUsers'] 
                    clm['District'].append(dist)
                    clm['Registered_users'].append(count)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
                
#Succesfully created a dataframe
Map_Users=pd.DataFrame(clm)


#Dataframe for Top Transaction
path_top_tran = r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/pulse-master/data/top/transaction/country/india/state/"
top_tran_list=os.listdir(path_top_tran)

clm={'State':[], 'Year':[],'Quater':[],'Pincodes':[], 'Transaction_count':[], 'Transaction_amount':[]}
for i in top_tran_list:
    p_i=path_top_tran+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['pincodes']:
                Name=z['entityName']
                count=z['metric']['count']
                amount=z['metric']['amount']
                clm['Pincodes'].append(Name)
                clm['Transaction_count'].append(count)
                clm['Transaction_amount'].append(amount)
                clm['State'].append(i)
                clm['Year'].append(j)
                clm['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
Top_Trans=pd.DataFrame(clm)


#Dataframe for Top user
path_top_user = r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/pulse-master/data/top/user/country/india/state/"
Top_user_list=os.listdir(path_top_user)


clm={'State':[], 'Year':[],'Quater':[],'Pincode':[], 'Registered_users':[]}
for i in Top_user_list:
    p_i=path_top_user+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            #print(D)
            for z in D['data']['pincodes']:
                    dist=z['name']
                    count=z['registeredUsers'] 
                    clm['Pincode'].append(dist)
                    clm['Registered_users'].append(count)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
                
#Succesfully created a dataframe
Top_Users=pd.DataFrame(clm)

#sql connection
connection = sqlite3.connect("PhonePe.db")
curs = connection.cursor()
Agg_Trans.to_sql("Aggregate_Transaction",connection,if_exists='replace')
Agg_Users.to_sql("Aggregate_User",connection,if_exists='replace')
Map_Trans.to_sql("Map_Transaction",connection,if_exists='replace')
Map_Users.to_sql("Map_User",connection,if_exists='replace')
Top_Trans.to_sql("Top_Transaction",connection,if_exists='replace')
Top_Users.to_sql("Top_User",connection,if_exists='replace')


# Create the options
SELECT = option_menu(
    menu_title = None,
    options = ["Home","About","Project Details","Basic insights"],
    icons =["house","globe","bar-chart","toggles"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "white","size":"cover",'width':'100%'},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"},}
    )



# when we click the basic insights
if SELECT == "Basic insights":
    st.title("BASIC INSIGHTS")
    st.write("----")
    st.subheader("Let's know some basic insights about the data")
    st.write("----")
    st.sidebar.header(":wave: :violet[**Hello! Welcome to the dashboard**]")
    with st.sidebar:
        selected = option_menu("Menu", ["Top Charts","Explore Data","Geo Visualization"], 
                icons=["graph-up-arrow","bar-chart-line","geo"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin": "-1px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
    
    # 10 drop down questions
    if selected == "Explore Data":
        options = ["--select--","Top 10 states based on year and amount of transaction",
               "Least 10 States based on year and amount of transaction",
               "Top 10 states based on type and amount of transaction",
               "Least 10 states based on type and amount of transaction",
               "Top 5 Transaction_Type based on Transaction_Amount",
               "Least 5 Transaction_Type based on Transaction_Amount",
               "Top 10 Registered_users based on States and District",
               "Least 10 Registered_users based on states and District",
               "Top 10 Districts based on States and Count of Transaction",
               "Least 10 Districts based on states and count of transaction",
               "Top 10 mobile brands based on the percentage of the transaction",
               "Least 10 mobile brands based on the percentage of the transaction",
               "Top 10 Users based on user brand and state",
               "Least 10 Users based on user brand and state",
               "Top 10 Registered Users based on pincodes and State",
               "Least 10 Registered Users based on pincodes and State"]
    
    
    
    
        # select box to select the options
        select = st.selectbox("Please select the option:",options)
        table = st.button(label = "Table and Distribution") # to show the distribution when we click this button
    
        
        # Answer for the first drop down question
        def query1():
            query1 = """SELECT State,Year,SUM(Transaction_amount) AS Total_Transaction_Amount FROM Top_Transaction GROUP BY State,Year ORDER BY Total_Transaction_Amount DESC LIMIT 10"""

            curs.execute(query1)
            data=curs.fetchall()
            df = pd.DataFrame(data)
            df=df.rename(columns = {0:"State",1:"Transaction_Year",2:"Transaction_Amount"})
            st.title("Top 10 states based on year and amount of transaction")
            col1,col2 = st.columns([1,1.5],gap = 'small')
            with col1:
                st.write(df)
            with col2:
                fig = px.bar(df,
                             x="State",
                             y="Transaction_Amount",
                             title = 'Top 10',
                             orientation='v',
                             color='Transaction_Amount',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig)              
                #st.bar_chart(df,x = "State",y = "Transaction_Amount")
        
        
        # Answer for the 2 drop down question
        def query2(): 
            query2 = """SELECT State,Year,SUM(Transaction_amount) AS Total_Transaction_Amount From Top_Transaction GROUP BY State,Year ORDER BY Total_Transaction_Amount LIMIT 10"""
        
            curs.execute(query2)
            data = curs.fetchall()
            df = pd.DataFrame(data)
            df=df.rename(columns = {0:"State",1:"Transaction_Year",2:"Transaction_Amount"})
            st.title("Least 10 states based on year and amount of transaction")
            col1,col2 = st.columns([1,1.5],gap = 'small')
            with col1:
                st.write(df)
            with col2:
                fig = px.bar(df,
                             x="State",
                             y="Transaction_Amount",
                             title = 'Least 10',
                             orientation='v',
                             color='Transaction_Amount',
                             color_continuous_scale=px.colors.sequential.Brwnyl)
                st.plotly_chart(fig)  
                #st.bar_chart(data = df,x = "State",y = "Transaction_Amount")
            
        # Answer for the 3rd question
        def query3():
            query3 = """SELECT State,Transaction_type,SUM(Transaction_amount) AS Total_Transaction_Amount FROM Aggregate_Transaction GROUP BY State,Transaction_Type ORDER BY Total_Transaction_Amount DESC LIMIT 10"""

            curs.execute(query3)
            data = curs.fetchall()
            df3 = pd.DataFrame(data)
            df3 = df3.rename(columns = {0:"State",1:"Transaction_Type",2:"Total_Transaction_Amount"})
            st.title("Top 10 states based on type and amount of transaction")
            col1,col2 =st.columns([1,1.5],gap = 'small')
            with col1:
                st.write(df3)
            with col2:
                fig = px.bar(df3,
                             x="State",
                             y="Total_Transaction_Amount",
                             title = 'Top 10',
                             orientation='v',
                             color='Total_Transaction_Amount',
                             color_continuous_scale=px.colors.sequential.Bluyl)
                st.plotly_chart(fig) 
                
                
        # Answer for the 4th question
        def query4():
            query4 = """SELECT State,Transaction_type,SUM(Transaction_amount) AS Total_Transaction_Amount FROM Aggregate_Transaction GROUP BY State,Transaction_Type ORDER BY Total_Transaction_Amount LIMIT 10"""

            curs.execute(query4)
            data = curs.fetchall()
            df4 = pd.DataFrame(data)
            df4 = df4.rename(columns={0:"State",1:"Transaction_Type",2:"Total_Transaction_Amount"})
            st.title("Least 10 states based on type and amount of transaction")
            col1,col2 = st.columns([1,1.5],gap = 'small')
            with col1:
                st.write(df4)
            with col2:
                fig = px.bar(df4,
                             x="State",
                             y="Total_Transaction_Amount",
                             orientation='v',
                             title = 'Least 10',
                             color='Total_Transaction_Amount',
                             color_continuous_scale=px.colors.sequential.Burg)
                st.plotly_chart(fig)
           
        # Answer for the 5th question
        def query5():
            query5 = """SELECT Transaction_Type,SUM(Transaction_amount) AS Total_Transaction_Amount FROM Aggregate_Transaction GROUP BY Transaction_Type ORDER BY Total_Transaction_Amount DESC LIMIT 5"""

            curs.execute(query5)
            data = curs.fetchall()
            df5 = pd.DataFrame(data)
            df5 = df5.rename(columns={0:"Transaction_Type",1:"Total_Transaction_Amount"})
            st.title("Top 5 Transaction_Type based on Transaction_Amount")
            col1,col2 = st.columns([1,1.5],gap = 'small')
            with col1:
                st.write(df5)
            with col2:
                fig = px.bar(df5,
                             x="Transaction_Type",
                             y="Total_Transaction_Amount",
                             orientation='v',
                             title = 'Top 10',
                             color='Total_Transaction_Amount',
                             color_continuous_scale=px.colors.sequential.Burgyl)
                st.plotly_chart(fig)
            

        # Answer for the 6th question
        def query6():
            query6 = """SELECT Transaction_Type,SUM(Transaction_amount) AS Total_Transaction_Amount FROM Aggregate_Transaction GROUP BY Transaction_Type ORDER BY Total_Transaction_Amount LIMIT 5"""

            curs.execute(query6)
            data = curs.fetchall()
            df6 = pd.DataFrame(data)
            df6 = df6.rename(columns={0:"Transaction_Type",1:"Total_Transaction_Amount"})
            st.title("Least 5 Transaction_Type based on Transaction_Amount")
            col1,col2 = st.columns([1,1.5],gap = 'small')
            with col1:
                st.write(df6)
            with col2:
                fig = px.bar(df6,
                             x="Transaction_Type",
                             y="Total_Transaction_Amount",
                             orientation='v',
                             title = 'Least 10',
                             color='Total_Transaction_Amount',
                             color_continuous_scale=px.colors.sequential.Cividis)
                st.plotly_chart(fig)

        # Answer for the 7th question
        def query7():
            query7 = """SELECT State,District,SUM(Registered_users) AS Total_Registered_users FROM Map_User GROUP BY State,District ORDER BY Total_Registered_users DESC LIMIT 10"""

            curs.execute(query7)
            data = curs.fetchall()
            df7 = pd.DataFrame(data)
            df7 = df7.rename(columns = {0:"State",1:"District",2:"Total_Registered_Users"})
            st.title("Top 10 Registered_users based on States and District")
            col1,col2 = st.columns([1,1.5],gap = 'small')
            with col1:
                st.write(df7)
            with col2:
                fig = px.bar(df7,
                             x="District",
                             y="Total_Registered_Users",
                             orientation='v',
                             title = 'Top 10',
                             color='Total_Registered_Users',
                             color_continuous_scale=px.colors.sequential.Darkmint)
                st.plotly_chart(fig)

        # Answer for the 8th question
        def query8():
            query8 = """SELECT State,District,SUM(Registered_users) AS Total_Registered_users FROM Map_User GROUP BY State,District ORDER BY Total_Registered_users LIMIT 10"""

            curs.execute(query8)
            data = curs.fetchall()
            df8 = pd.DataFrame(data)
            df8 = df8.rename(columns = {0:"State",1:"District",2:"Total_Registered_Users"})
            st.title("Least 10 Registered_users based on States and District")
            col1,col2 = st.columns([1,1.5],gap = 'small')
            with col1:
                st.write(df8)
            with col2:
                fig = px.bar(df8,
                             x="District",
                             y="Total_Registered_Users",
                             orientation='v',
                             title = 'Least 10',
                             color='Total_Registered_Users',
                             color_continuous_scale=px.colors.sequential.Electric)
                st.plotly_chart(fig)

        # Answer for the 9th question
        def query9():
            query9 = """SELECT District_Name,State,SUM(Distict_Transaction_count) AS Total_Transaction_Count FROM Map_Transaction GROUP BY District_Name,State ORDER BY Total_Transaction_Count DESC LIMIT 10"""

            curs.execute(query9)
            data = curs.fetchall()
            df9 = pd.DataFrame(data)
            df9 = df9.rename(columns={0:"District",1:"State",2:"Total_Transaction_Count"})
            st.title("Top 10 Districts based on states and count of transaction")
            col1,col2 = st.columns([1,1.5],gap = 'small')
            with col1:
                st.write(df9)
            with col2:
                fig = px.bar(df9,
                             x="District",
                             y="Total_Transaction_Count",
                             orientation='v',
                             title = 'Top 10',
                             color='Total_Transaction_Count',
                             color_continuous_scale=px.colors.sequential.Emrld)
                st.plotly_chart(fig)


        # Answer for the 10th question
        def query10():
            query10 = """SELECT District_Name,State,SUM(Distict_Transaction_count) AS Total_Transaction_Count FROM Map_Transaction GROUP BY District_Name,State ORDER BY Total_Transaction_Count LIMIT 10"""

            curs.execute(query10)
            data = curs.fetchall()
            df10 = pd.DataFrame(data)
            df10 = df10.rename(columns={0:"District",1:"State",2:"Total_Transaction_Count"})
            st.title("Least 10 Districts based on states and count of transaction")
            col1,col2 = st.columns([1,1.5],gap = 'small')
            with col1:
                st.write(df10)
            with col2:
                fig = px.bar(df10,
                             x="District",
                             y="Total_Transaction_Count",
                             orientation='v',
                             title = 'Least 10',
                             color='Total_Transaction_Count',
                             color_continuous_scale=px.colors.sequential.Greens)
                st.plotly_chart(fig)

        # Answer for the 11th question
        def query11():
            query11 = """SELECT User_Brand,SUM(User_Percentage) AS Total_User_Percentage FROM Aggregate_User GROUP BY User_Brand ORDER BY Total_User_Percentage DESC LIMIT 10"""

            curs.execute(query11)
            data = curs.fetchall()
            df11 = pd.DataFrame(data)
            df11 = df11.rename(columns={0:"User_Brand",1:"Total_Percentage"})
            st.title("Top 10 mobile brands based on the percentage of the transaction")
            col1,col2 = st.columns([1,1.5],gap = 'small')
            with col1:
                st.write(df11)
            with col2:
                fig = px.bar(df11,
                             x="User_Brand",
                             y="Total_Percentage",
                             orientation='v',
                             title = 'Top 10',
                             color='Total_Percentage',
                             color_continuous_scale=px.colors.sequential.Hot)
                st.plotly_chart(fig)
    
        # Answer for the 12th question
        def query12():
            query12 = """SELECT User_Brand,SUM(User_Percentage) AS Total_User_Percentage FROM Aggregate_User GROUP BY User_Brand ORDER BY Total_User_Percentage LIMIT 10"""
    
            curs.execute(query12)
            data = curs.fetchall()
            df12 = pd.DataFrame(data)
            df12 = df12.rename(columns={0:"User_Brand",1:"Total_Percentage"})
            st.title("Least 10 mobile brands based on the percentage of the transaction")
            col1,col2 = st.columns(2)
            with col1:
                st.write(df12)
            with col2:
                fig = px.bar(df12,
                             x="User_Brand",
                             y="Total_Percentage",
                             orientation='v',
                             title = 'Least 10',
                             color='Total_Percentage',
                             color_continuous_scale=px.colors.sequential.Inferno)
                st.plotly_chart(fig)
    

        # Answer for the 13 th question
        def query13():
            query13 = """SELECT User_Brand,State,SUM(User_Count) AS Total_User_Count FROM Aggregate_User GROUP BY State,User_Brand ORDER BY Total_User_Count DESC LIMIT 10"""

            curs.execute(query13)
            data = curs.fetchall()
            df13 = pd.DataFrame(data)
            df13 = df13.rename(columns={0:"User_Brand",1:"State",2:"Total_User_count"})
            st.title("Top 10 Users based on user brand and state")
            col1,col2 = st.columns([1,1.5],gap = 'small')
            with col1:
                st.write(df13)
            with col2:
                fig = px.bar(df13,
                             x="User_Brand",
                             y="Total_User_count",
                             orientation='v',
                             title = 'Top 10',
                             color='Total_User_count',
                             color_continuous_scale=px.colors.sequential.Jet)
                st.plotly_chart(fig)

        # Answer for the 14th question
        def query14():
            query14 = """SELECT User_Brand,State,SUM(User_Count) AS Total_User_Count FROM Aggregate_User GROUP BY State,User_Brand ORDER BY Total_User_Count LIMIT 10"""

            curs.execute(query14)
            data = curs.fetchall()
            df14 = pd.DataFrame(data)
            df14 = df14.rename(columns={0:"User_Brand",1:"State",2:"Total_User_count"})
            st.title("Least 10 Users based on user brand and state")
            
            col1,col2 = st.columns([1,1.5],gap = 'small')
            with col1:
                st.write(df14)
            with col2:
                fig = px.bar(df14,
                             x="User_Brand",
                             y="Total_User_count",
                             orientation='v',
                             title = 'Least 10',
                             color='Total_User_count',
                             color_continuous_scale=px.colors.sequential.Magenta)
                st.plotly_chart(fig)


        # Answer for the 15th question
        def query15():
            query15 = """SELECT State,Pincode,SUM(Registered_users) AS Total_Registered_users FROM Top_User GROUP BY State,Pincode ORDER BY Total_Registered_users DESC LIMIT 10"""

            curs.execute(query15)
            data = curs.fetchall()
            df15 = pd.DataFrame(data)
            df15 = df15.rename(columns={0:"State",1:"Pincode",2:"Total_Registered_users"})
            st.title("Top 10 Registered Users based on pincodes and State")
            col1,col2 = st.columns([1,1.5],gap = 'small')
            with col1:
                st.write(df15)
            with col2:
                fig = px.bar(df15,
                             x="State",
                             y="Total_Registered_users",
                             orientation='v',
                             title = 'Top 10',
                             color='Total_Registered_users',
                             color_continuous_scale=px.colors.sequential.Magma)
                st.plotly_chart(fig)


        # Answer for the 16th question
        def query16():
            query16 = """SELECT State,Pincode,SUM(Registered_users) AS Total_Registered_users FROM Top_User GROUP BY State,Pincode ORDER BY Total_Registered_users LIMIT 10"""

            curs.execute(query16)
            data = curs.fetchall()
            df16 = pd.DataFrame(data)
            df16 = df16.rename(columns={0:"State",1:"Pincode",2:"Total_Registered_users"})
            st.title("Least 10 Registered Users based on pincodes and State")
            col1,col2 = st.columns([1,1.5],gap = 'small')
            with col1:
                st.write(df16)
            with col2:
                fig = px.bar(df16,
                             x="State",
                             y="Total_Registered_users",
                             title = 'Least 10',
                             orientation='v',
                             color='Total_Registered_users',
                             color_continuous_scale=px.colors.sequential.Mint)
                st.plotly_chart(fig)
            #st.bar_chart(data =df16,x = 'Pincode',y='Total_Registered_users')

        # If we click the table button
        if table:
            ind = options.index(select) # find the index of the drop down question
            if ind == 0:
                st.write("Please select any option")
            elif ind == 1:
                query1()
            elif ind == 2:
                query2()
            elif ind == 3:
                query3()
            elif ind == 4:
                query4()
            elif ind == 5:
                query5()
            elif ind == 6:
                query6()
            elif ind == 7:
                query7()
            elif ind == 8:
                query8()
            elif ind==9:
                query9()
            elif ind==10:
                query10()
            elif ind == 11:
                query11()
            elif ind == 12:
                query12()
            elif ind == 13:
                query13()
            elif ind == 14:
                query14()
            elif ind == 15:
                query15()
            else:
                query16()
    
    
    # If selected the one of the menu's in the basic insights
    if selected == "Top Charts":
        st.markdown("## :violet[Top Charts]")
        Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users")) # create the side bar
        col1,col2 = st.columns([1,1.5],gap='large')
        with col1:
            Year = st.slider("**Year**",min_value = 2018, max_value = 2023) # create the slider
            Quarter = st.slider("Quarter",min_value = 1, max_value = 4) # create the slider

        with col2: # create the short notes about the top charts
            st.info("""
            ### From this menu we can get insights like:
            - Overall ranking on a particular Year and Quarter.
            - Top 10 State, District,Pincode based on a Total number of transaction and Total amount spent on phonepe
            - Top 10 State, District,Pincode based on Total Phonepe users and their app opening frequency
            - Top 10 mobile brands and its percentage based on how many people use phonepe.
                    """,icon = "🔍")


        # If we click the transaction type
        if Type == "Transactions":
            col1,col2= st.columns([1,1],gap = "small")
            col3,col4=st.columns([1,1],gap = 'small')
            if Year==2023 and Quarter in [3,4]: 
                    st.markdown("Sorry no data to display for 2023 Quarter 3,4")
            else:
                with col1:
                    st.markdown("### :violet[States]")
                    curs.execute(f"SELECT State,SUM(Transaction_count) as Total_Transaction_count,SUM(Transaction_amount) as Total_Transaction_amount FROM Aggregate_Transaction where Year = {Year} and Quater = {Quarter} GROUP BY State ORDER BY Total_Transaction_amount DESC LIMIT 10")
                    data = curs.fetchall()
                    df = pd.DataFrame(data)
                    df = df.rename(columns = {0:"State",1:"Transaction_Count",2:"Total_Transaction_Amount"})
                    fig = px.pie(df,values = "Total_Transaction_Amount",
                             names = "State",
                             title = "Top 10",
                             color_discrete_sequence = px.colors.sequential.Aggrnyl,hover_data = ['Transaction_Count'],
                             labels = {'Transaction_Count':'Transaction_Count'})

                    fig.update_traces(textposition = 'inside',textinfo = 'percent+label')
                    st.plotly_chart(fig,use_container_width = True)

                with col2:
                    st.markdown("### :violet[Districts]")
                    curs.execute(f"SELECT District_Name,SUM(Distict_Transaction_count) as Total_Transaction_count,SUM(District_Transaction_amount) as Total_Transaction_amount FROM Map_Transaction where Year = {Year} and Quater = {Quarter} GROUP BY District_Name ORDER BY Total_Transaction_amount DESC LIMIT 10")
                    data = curs.fetchall()
                    df = pd.DataFrame(data)
                    df = df.rename(columns = {0:"District",1:"Transaction_Count",2:"Total_Transaction_Amount"})
                    fig = px.pie(df,values = "Total_Transaction_Amount",
                                 names = "District",
                             title = "Top 10",
                             color_discrete_sequence = px.colors.sequential.Agsunset,hover_data = ['Transaction_Count'],
                             labels = {'Transaction_Count':'Transaction_Count'})

                    fig.update_traces(textposition = 'inside',textinfo = 'percent+label')
                    st.plotly_chart(fig,use_container_width = True)

                with col3:
                    st.markdown("### :violet[Pincodes]")
                    curs.execute(f"SELECT Pincodes,State,SUM(Transaction_count) as Total_Transaction_count,SUM(Transaction_amount) as Total_Transaction_amount FROM Top_Transaction where Year = {Year} and Quater = {Quarter} GROUP BY Pincodes,State ORDER BY Total_Transaction_amount DESC LIMIT 10")
                    data = curs.fetchall()
                    df = pd.DataFrame(data)
                    df = df.rename(columns = {0:"Pincodes",1:"State",2:"Transaction_Count",3:"Total_Transaction_Amount"})
                    fig = px.pie(df,values = "Total_Transaction_Amount",
                             names = "Pincodes",
                             title = "Top 10",
                             color_discrete_sequence = px.colors.sequential.Blues,hover_data = ['State'],
                             labels = {'Transaction_Count':'Transaction_Count'})

                    fig.update_traces(textposition = 'inside',textinfo = 'percent+label')
                    st.plotly_chart(fig,use_container_width = True)



        if Type == "Users":
            col1,col2 = st.columns([1,1],gap = "large")
            col3,col4 = st.columns([1,1],gap = "large")

            if Year == 2023 and Quarter in [3,4]:
                st.markdown("###### Sorry No data to display for 2023 Qtr 3,4")
            else:
                with col1:
                    st.markdown("### :violet[Brands]")
                    try:
                        curs.execute(f"SELECT User_Brand,SUM(User_Count) as Total_User_Count,AVG(User_Percentage)*100 AS Avg_Percentage FROM Aggregate_User where Year = {Year} and Quater = {Quarter} GROUP BY User_Brand ORDER BY Total_User_Count DESC LIMIT 10")
                        data = curs.fetchall()
                        df = pd.DataFrame(data)
                        df = df.rename(columns = {0:"Brands",1:"Total_users",2:"Average_usage"})
                        fig = px.pie(df,values = "Average_usage",
                                 names = "Brands",
                                 title = "Top 10",
                                 color_discrete_sequence = px.colors.sequential.Bluered,hover_data = ['Total_users'],
                                 labels = {'Average_usage':'Average_usage'})

                        fig.update_traces(textposition = 'inside',textinfo = 'percent+label')
                        st.plotly_chart(fig,use_container_width = True)
                    except:
                        st.markdown("There is no data in this Quarter or Year.Please change the Quarter for your understanding")


                with col2:
                    st.markdown("### :violet[District]")
                    try:
                        curs.execute(f"SELECT District,SUM(Registered_users) as Total_Users FROM Map_User where Year = {Year} and Quater = {Quarter} GROUP BY District ORDER BY Total_Users DESC LIMIT 10")
                        data = curs.fetchall()
                        df = pd.DataFrame(data)
                        df = df.rename(columns = {0:"District",1:"Total_users"})
                        fig = px.pie(df,values = "Total_users",
                                 names = "District",
                                 title = "Top 10",
                                 color_discrete_sequence = px.colors.sequential.Blackbody,hover_data = ['Total_users'],
                                 labels = {'Total_users':'Total_users'})

                        fig.update_traces(textposition = 'inside',textinfo = 'percent+label')
                        st.plotly_chart(fig,use_container_width = True)
                    except:
                        st.markdown("There is no data in this Quarter or Year.Please change the Quarter for your understanding")


                with col3:
                    st.markdown("### :violet[Pincode]")
                    try:
                        curs.execute(f"SELECT Pincode,SUM(Registered_users) as Total_Users FROM Top_User where Year = {Year} and Quater = {Quarter} GROUP BY Pincode ORDER BY Total_Users DESC LIMIT 10")
                        data = curs.fetchall()
                        df = pd.DataFrame(data)
                        df = df.rename(columns = {0:"Pincodes",1:"Total_users"})
                        fig = px.pie(df,values = "Total_users",
                                 names = "Pincodes",
                                 title = "Top 10",
                                 color_discrete_sequence = px.colors.sequential.Blugrn,hover_data = ['Total_users'],
                                 labels = {'Total_users':'Total_users'})

                        fig.update_traces(textposition = 'inside',textinfo = 'percent+label')
                        st.plotly_chart(fig,use_container_width = True)
                    except:
                        st.markdown("There is no data in this Quarter or Year.Please change the Quarter for your understanding")


                with col4:
                    st.markdown("### :violet[State]")
                    try:
                        curs.execute(f"SELECT State,SUM(Registered_users) as Total_Users FROM Map_User where Year = {Year} and Quater = {Quarter} GROUP BY State ORDER BY Total_Users DESC LIMIT 10")
                        data = curs.fetchall()
                        df = pd.DataFrame(data)
                        df = df.rename(columns = {0:"State",1:"Total_users"})
                        fig = px.pie(df,values = "Total_users",
                                 names = "State",
                                 title = "Top 10",
                                 color_discrete_sequence = px.colors.sequential.Purples,hover_data = ['Total_users'],
                                 labels = {'Total_users':'Total_users'})

                        fig.update_traces(textposition = 'inside',textinfo = 'percent+label')
                        st.plotly_chart(fig,use_container_width = True)
                    except:
                        st.markdown("There is no data in this Quarter or Year.Please change the Quarter for your understanding")

                        
    # to show the geo visualization of the data
    if selected == "Geo Visualization":
        st.markdown("## :violet[Geo Visualization]")
        Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
        col1,col2 = st.columns([1,1.5],gap='large')
        with col1:
            Year = st.slider("**Year**",min_value = 2018, max_value = 2023)
            Quarter = st.slider("Quarter",min_value = 1, max_value = 4)

        with col2:
            st.info("""
            ### From this menu we can get insights like:
            - Overall ranking on a particular Year and Quarter.
            - All State, District,Pincode based on a Total number of transaction and Total amount spent on phonepe
            - All State, District,Pincode based on Total Phonepe users and their app opening frequency
                    """,icon = "🔍")
                
        if Type == "Transactions":
            distribution = ['--select','Transaction_Amount','Transaction_Count']
            box = st.selectbox("Please select the option ",distribution)
            
            def state():
                st.markdown("## :violet[Overall State Data - Transactions Amount]")
                curs.execute(f"SELECT State,SUM(Distict_Transaction_count) as Total_Transactions,SUM(District_Transaction_amount) as Total_amount from Map_Transaction where Year = {Year} and Quater = {Quarter} group by State order by State")
                df1 = pd.DataFrame(curs.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
                df2 = pd.read_csv(r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/pulse-master/data/Statenames.csv")
                df1.State = df2

                fig =  px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='Total_amount',
                color_continuous_scale='pubu',width = 10000,height = 500,projection = 'baker')

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig,use_container_width=True)
                
                
            def state_count():    
                st.markdown("## :violet[Overall State Data - Transactions Count]")
                curs.execute(f"SELECT State,SUM(Distict_Transaction_count) as Total_Transactions,SUM(District_Transaction_amount) as Total_amount from Map_Transaction where Year = {Year} and Quater = {Quarter} group by State order by State")
                df3 = pd.DataFrame(curs.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
                df4 = pd.read_csv(r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/pulse-master/data/Statenames.csv")
                df3.State = df4

                fig =  px.choropleth(df3,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='Total_Transactions',
                color_continuous_scale='blackbody',width = 10000,height = 500,projection = 'baker')

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig,use_container_width=True)
            
            if box:
                ind = distribution.index(box)
                if ind == 0:
                    st.markdown("Please select any option")
                elif ind == 1:
                    state()
                else:
                    state_count()
                    
        if Type == "Users":
            distribution = ['--select','Registered_Users','User_percentage']
            box = st.selectbox("Please select the option ",distribution)
            
            def reg():
                st.markdown("## :violet[Overall State Data - Registered Users]")
                curs.execute(f"SELECT State,SUM(Registered_users) as Total_User_count from Map_User where Year = {Year} and Quater = {Quarter} group by State order by State")
                df1 = pd.DataFrame(curs.fetchall(),columns= ['State', 'Total_User_count'])
                df2 = pd.read_csv(r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/pulse-master/data/Statenames.csv")
                df1.State = df2

                fig =  px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='Total_User_count',
                color_continuous_scale='portland',width = 10000,height = 500,projection = 'baker')

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig,use_container_width=True)
                
                
            def perc():    
                st.markdown("## :violet[Overall State Data - User_Percentage]")
                curs.execute(f"SELECT State,Avg(User_Percentage)*100 as User_Percentage from Aggregate_User where Year = {Year} and Quater = {Quarter} group by State,User_Brand order by State")
                df3 = pd.DataFrame(curs.fetchall(),columns= ['State','User_Percentage'])
                df4 = pd.read_csv(r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/pulse-master/data/Statenames.csv")
                df3.State = df4

                fig =  px.choropleth(df3,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='User_Percentage',
                color_continuous_scale='agsunset',width = 10000,height = 500,projection = 'baker')

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig,use_container_width=True)
            
            if box:
                ind = distribution.index(box)
                if ind == 0:
                    st.markdown("Please select any option")
                elif ind == 1:
                    reg()
                else:
                    perc()
                             

            
    

# if we select the home menu
if SELECT == "Home":
    st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    .big-font {
    font-size:300px !important;
}
    </style>
    """,
    unsafe_allow_html=True
    )
    
    col1,col2, = st.columns([2,1],gap = 'large')
    with col1:
        st.header(":violet[Phonepe Data Visualization]")
        add_vertical_space(2)
        st.write("""**PhonePe has launched PhonePe Pulse, a data analytics platform that provides insights into
                        how Indians are using digital payments. With over 30 crore registered users and 2000 crore 
                        transactions, PhonePe, India's largest digital payments platform with 46% UPI market share,
                        has a unique ring-side view into the Indian digital payments story. Through this app, you 
                        can now easily access and visualize the data provided by PhonePe Pulse, gaining deep 
                        insights and interesting trends into how India transacts with digital payments.**""")
        add_vertical_space(1)
        
        st.download_button(":blue[DOWNLOAD THE APP NOW]", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open("Images/image_phonepe.webp"),width = 300)
        
        
    add_vertical_space(2)
    st.header(":violet[Essential Services on Phonepe]")
    st.video("Images/phonepe_video.mp4")
    add_vertical_space(2)
    
    st.header(":violet[Digital Payment Growth in India]")
    col1,col2 = st.columns([1,1],gap = 'small')
    with col1:
        st.image(Image.open("Images/digital_payments.jpg"),width = 520)
    
    with col2:
        st.image(Image.open("Images/digit_pay3.png"))
        
    
    add_vertical_space(4)
    st.header(":violet[Metric data of PhonePe]")
    col1,col2,col3 = st.columns([1,1,1],gap = 'small')
    curs.execute("""SELECT SUM(Registered_users) FROM Map_User""")
    data = curs.fetchall()
    df = pd.DataFrame(data)
    df =df.rename(columns = {0:'reg_user'})
    total_reg_users = df['reg_user'][0]
    col1.metric(
            label = 'Total Registered Users',
            value = '{:.2f} Cr'.format(total_reg_users/100000000),
            delta = 'Forward Trend'
            )
    
    curs.execute("""SELECT SUM(Transaction_count) FROM Aggregate_Transaction""")
    data = curs.fetchall()
    df = pd.DataFrame(data)
    df =df.rename(columns = {0:'reg_user'})
    total_tran = df['reg_user'][0]
    col2.metric(
            label = 'Total Transaction Count',
            value = '{:.2f} Cr'.format(total_tran/100000000),
            delta = 'Forward Trend'
            )
    curs.execute("""SELECT SUM(Transaction_amount) FROM Aggregate_Transaction""")
    data = curs.fetchall()
    df = pd.DataFrame(data)
    df =df.rename(columns = {0:'reg_user'})
    tot_amo = df['reg_user'][0]
    col3.metric(
            label = 'Total Transaction Amount',
            value = '{:.2f} Cr'.format(tot_amo/100000000),
            delta = 'Forward Trend'
            )
    style_metric_cards(background_color='200329')
    
    
    st.header(":violet[Phonepe's Developement in last 7 years]")
    Year = st.slider("**Year**",min_value = 2016, max_value = 2022)
    if Year == 2016:
        st.image(Image.open("Images/2016.png"))
    elif Year == 2017:
        st.image(Image.open("Images/2017.png"))
    elif Year == 2018:
        st.image(Image.open("Images/2018.png"))
    elif Year == 2019:
        st.image(Image.open("Images/2019.png"))
    elif Year == 2020:
        st.image(Image.open("Images/2020.png"))
    elif Year == 2021:
        st.image(Image.open("Images/2021.png"))
    else:
        st.image(Image.open("Images/2022.png"))
        

#If we click the about menu
if SELECT == 'About':
    add_vertical_space(4)
    st.header(":violet[_Introduction_]")
    add_vertical_space(2)
    st.markdown("**_The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government. Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. PhonePe Pulse is our way of giving back to the digital payments ecosystem._**")
    add_vertical_space(4)
    st.header(":violet[_Guide_]")
    st.markdown("**_This data has been structured to provide details on data cuts of Transactions and Users on the Explore tab._**")
    add_vertical_space(2)
    st.subheader(":violet[_1.Aggregated_]")
    add_vertical_space(1)
    st.markdown("**_Aggregated values of various payment categories as shown under Categories section_**")
    add_vertical_space(1)
    st.subheader(":violet[_The Categories :_]")
    st.markdown("**1.Recharge and bill payments**")
    st.markdown("**2.peer-to-peer payments**")
    st.markdown("**3.Merchant Payments**")
    st.markdown("**4.Financial services**")
    st.markdown("**5.Other payments**")
    add_vertical_space(2)
    st.subheader(":violet[_2.Map_]")
    add_vertical_space(1)
    st.markdown("**_Total values at the State and District levels_**")
    add_vertical_space(2)
    st.subheader(":violet[_3.Top_]")
    add_vertical_space(1)
    st.markdown("**_Totals of top States / Districts / Postal Codes_**")
    add_vertical_space(2)
    st.subheader(":violet[_Here we can download the data set as csv,json,excel_]")
    option = ["--select--","Aggregate_Transaction","Aggregate_User","Map Transaction","Map User","Top Transaction","Top User"]
    add_vertical_space(1)
    
    
    
    
    
    agg_trans_df = pd.read_csv(r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/csv_files/agg_trans.csv")
    agg_user_df = pd.read_csv(r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/csv_files/agg_user.csv")
    map_trans_df = pd.read_csv(r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/csv_files/map_tran.csv")
    map_user_df = pd.read_csv(r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/csv_files/map_user.csv")
    top_trans_df = pd.read_csv(r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/csv_files/top_tran.csv")
    top_user_df = pd.read_csv(r"C:/Users/subag/Downloads/Python 20.7/Project_2_Sample/csv_files/top_user.csv")
    
    
    
    tab = st.selectbox("Please select the option",option)
    table = st.button(label = 'Show Table')  
    if table:
        ind = option.index(tab)
        if ind == 0:
            st.write("Please select any option")
        elif ind == 1:
            st.write(agg_trans_df)
            c = agg_trans_df
        elif ind == 2:
            st.write(agg_user_df)
            c = agg_user_df
        elif ind == 3:
            st.write(map_trans_df)
            c = map_trans_df
        elif ind == 4:
            st.write(map_user_df)
            c = map_user_df
        elif ind == 5:
            st.write(top_trans_df)
            c = top_trans_df
        else:
            st.write(top_user_df)
            c = top_user_df
                        
        col1,col2,col3 = st.columns([1,1,1],gap = 'small')
        with col1:
            add_vertical_space(4)
            def convert_df(c):
                return c.to_csv(index=False).encode('utf-8')        
            csv = convert_df(c)
            st.download_button(":blue[Download csv]",csv)
        with col2:
            add_vertical_space(4)
            def conv_df_j(c):
                return c.to_json(orient = 'records')
            json = conv_df_j(c)
            st.download_button(":blue[Download json]",json)
        with col3:
            add_vertical_space(4)
            def con_ex(c):
                excel_buffer = io.BytesIO()
                c.to_excel(excel_buffer, engine ='xlsxwriter', index = False)
                return excel_buffer.getvalue()
            xl = con_ex(c)
            st.download_button(":blue[Download Excel]",xl)

#if we click the Project details menu
if SELECT == "Project Details":
    st.title(":violet[PhonePe Pulse Data Visualization and Exploration]")
    st.write("----")
    st.subheader("A User-Friendly Tool Using Streamlit and Plotly")
    st.write("----")     
    st.subheader(":violet[Technologies]")
    add_vertical_space(1)
    st.markdown("**1.Github Cloning**")
    st.markdown("**2.Python**")
    st.markdown("**3.Pandas**")
    st.markdown("**4.MySQL**")
    st.markdown("**5.mysql-connector-python**")
    st.markdown("**6.Streamlit**")
    st.markdown("**7.Plotly**")
    add_vertical_space(1)
    st.subheader(":violet[Problem Statement]")
    st.markdown("**The PhonePe pulse Github repository contains a large amount of data related to various metrics and statistics. The goal is to extract this data and process it to obtain insights and information that can be visualized in a user friendly manner**")
    add_vertical_space(1)
    st.subheader(":violet[Approach]")
    st.subheader(":blue[Data Extraction]")
    st.markdown("**Clone the Github using scripting to fetch the data from the Phonepe pulse Github repository and store it in a suitable format such as CSV or JSON.**")
    add_vertical_space(1)
    st.subheader(":blue[Data Transformation]")
    st.markdown("**Use a scripting language such as Python, along with libraries such as Pandas, to manipulate and pre-process the data. This may include cleaning the data, handling missing values, and transforming the data into a format suitable for analysis and visualization.**")
    add_vertical_space(1)
    st.subheader(":blue[Database Insertion]")
    st.markdown("**Use the 'mysql-connector-python' library in Python to connect to a MySQL database and insert the transformed data using SQL commands.**")
    add_vertical_space(1)
    st.subheader(":blue[Dashboard Creation]")
    st.markdown("**Use the Streamlit and Plotly libraries in Python to create an interactive and visually appealing dashboard. Plotly's built-in geo map functions can be used to display the data on a map and Streamlit can be used to create a user-friendly interface with multiple dropdown options for users to select different facts and figures to display.**")
    add_vertical_space(1)
    st.subheader(":blue[Data retrieval]")
    st.markdown("**Use the 'mysql-connector-python' library to connect to the MySQL database and fetch the data into a Pandas dataframe. Use the data in the dataframe to update the dashboard dynamically.**")
    add_vertical_space(1)
    st.subheader(":blue[Deployment]")
    st.markdown("**Ensure the solution is secure, efficient, and user-friendly. Test the solution thoroughly and deploy the dashboard publicly, making it accessible to users..**")
    
    add_vertical_space(2)
    st.subheader(":violet[Results]")
    st.markdown("**The result of this project will be a live geo visualization dashboard that displays information and insights from the Phonepe pulse Github repository in an interactive and visually appealing manner. The dashboard will have at least 10 different dropdown options for users to select different facts and figures to display. The data will be stored in a MySQL database for efficient retrieval and the dashboard will be dynamically updated to reflect the latest data.**")
    add_vertical_space(1)
    st.markdown("**Users will be able to access the dashboard from a web browser and easily navigate the different visualizations and facts and figures displayed. The dashboard will provide valuable insights and information about the data in the Phonepe pulse Github repository, making it a valuable tool for data analysis and decision-making.**")
    add_vertical_space(1)
    st.markdown("**Overall, the result of this project will be a comprehensive and user-friendly solution for extracting, transforming, and visualizing data from the Phonepe pulse Github repository.**")
    
    add_vertical_space(2)
    st.subheader(":violet[The Learning outcomes of the project]")
    add_vertical_space(1)
    st.markdown("**1.Data extraction and processing**")
    st.markdown("**2.Database Management**")
    st.markdown("**3.Visuaization and dashboard creation**")
    st.markdown("**4.Geo Visualization**")
    st.markdown("**5.Dynamic Updating**")
    st.markdown("**6.Project development and deployment**")
    
    
    add_vertical_space(2)
    st.header(":violet[DataSet]")
    st.markdown("**A home for the data that powers the PhonePe Pulse website.**")
    st.markdown("[Click here to open the dataset](https://github.com/PhonePe/pulse#readme)")
    
    add_vertical_space(2)
    st.header(":violet[App Demo]")
    st.markdown("**A home for the data that powers the PhonePe Pulse website.**")
    st.markdown("[Click here to open the App Demo](https://www.phonepe.com/pulse/explore/transaction/2022/4/)")
        
    
    
    
    
    
            
              
        