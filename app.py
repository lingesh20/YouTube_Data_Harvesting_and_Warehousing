import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import mongo
import api
import migratetosql
import pandas as pd
import analysisquery as analysis
import plotly.express as px 
import toml


st.set_page_config(page_title="YouTube Warehouse",page_icon="🧊", layout="wide")
left_column, right_column = st.columns(2)

channel_id = None

with left_column:
    st.title("YouTube Data Analysis")
    with st.container():
        channelId = st.text_input("Enter Channel ID to Checking Data Exist or not in Mongo")
        if channelId:
            retrieved_data = mongo.find_function(channelId)

    with st.container():
        channel_id = st.text_input("Enter Channel ID to Data reterving from Youtube Api")
        if channel_id:
            channel_data = api.retrieve_main(channel_id)
            st.write("Data fetched successfully!")

    with st.container():
        st.text("Store Data To MongoDb")
        try:
            if st.button("Store Data in MongoDB"):
                msg = mongo.store_function(channel_data)
                st.write(f"<span style='color: green;'>{msg}</span>", unsafe_allow_html=True)
        except:
            st.text("Please enter channel Id to retrive data")

    with st.container():
        channel_id = st.text_input("Enter Channel ID to Migrate Data to MySQL")
        if channel_id:
            try:
                message =  migratetosql.migrate_to_Sql(channel_id)
                st.success(message)
            except:
                st.write("<span style='color: red;'>Data already stored in MySQL Database</span>", unsafe_allow_html=True) 

    

    query_options = ['Tap view', '1. What are the names of all the videos and their corresponding channels?',
                        '2. Which channels have the most number of videos, and how many videos do they have?',
                        '3. What are the top 10 most viewed videos and their respective channels?',
                        '4. How many comments were made on each video, and what are their corresponding video names?',
                        '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
                        '6. What is the total number of likes for each video, and what are their corresponding video names?',
                        '7. What is the total number of views for each channel, and what are their corresponding channel names?',
                        '8. What are the names of all the channels that have published videos in the year 2022?',
                        '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
                        '10. Which videos have the highest number of comments, and what are their corresponding channel names?']
    
    select_question = st.selectbox("select the squestion", query_options)

with right_column:
    try:
        with st.container():
            if retrieved_data:
                st.subheader("Data Exist in MongoDB:")
                st.write("Channel Name:", retrieved_data['Channel_Name']['channel_name'])
            else:
                st.warning("Data not found in MongoDB Atlas!") 
    except:
        pass 

    try:
        with st.container():
            st.write("Channel Name:", channel_data['Channel_Name']['channel_name'])
            st.write("Channel ID:", channel_data['Channel_Name']['channel_id'])
            st.write("Subscription Count:", channel_data['Channel_Name']['subscriber_count'])
            st.write("Channel Views:", channel_data['Channel_Name']['channel_views'])
            st.write("Channel Description:", channel_data['Channel_Name']['channel_description'])
    except:
        pass

    try:
        with st.container():
            data = analysis.list_channel_names()
            if not data:
                st.info("The SQL database is currently empty")
            else:
                st.info("List of channels in SQL database")
                df = pd.DataFrame(data, columns=['Channel Name', 'Channel Subscription', 'Channel Views'])
                df.index+=1
                df
    except:
        pass

    try:
        with st.container():
            def question1():
                option = 1
                result = analysis.analysis_query(option)
                df = pd.DataFrame(result, columns=['Channel Name', 'Video Name']).reset_index(drop=True)
                df.index += 1
                return df
            def question2():
                option = 2
                result = analysis.analysis_query(option)
                df = pd.DataFrame(result, columns=['Channel Name', 'Video Count']).reset_index(drop=True)
                df.index += 1
                return df
            def question3():
                option = 3
                result = analysis.analysis_query(option)
                df = pd.DataFrame(result, columns=['Video Name', 'Channel Name', 'View Count']).reset_index(drop=True)
                df.index += 1
                return df
            def question4():
                option = 4
                result = analysis.analysis_query(option)
                df = pd.DataFrame(result, columns=['Video Name', 'Channel Name', 'Comment Count']).reset_index(drop=True)
                df.index += 1
                return df
            def question5():
                option = 5
                result = analysis.analysis_query(option)
                df = pd.DataFrame(result,  columns=['video Name', 'Channel Name', 'Like Count']).reset_index(drop=True)
                df.index += 1
                return df
            def question6():
                option = 6
                result = analysis.analysis_query(option)
                df = pd.DataFrame(result,  columns=['video Name', 'Like Count']).reset_index(drop=True)
                df.index += 1
                return df
            def question7():
                option = 7
                result = analysis.analysis_query(option)
                df = pd.DataFrame(result,  columns=['Channel Name', 'TotalViews']).reset_index(drop=True)
                df.index += 1
                return df
            def question8():
                option = 8
                result = analysis.analysis_query(option)
                df = pd.DataFrame(result, columns=['Channel Name']).reset_index(drop=True)
                df.index += 1
                return df
            def question9():
                option = 9
                result = analysis.analysis_query(option)
                df = pd.DataFrame(result, columns=['Channel Name', 'Avg duration of videos']).reset_index(drop=True)
                df.index += 1
                return df
            def question10():
                option = 10
                result = analysis.analysis_query(option)
                df = pd.DataFrame(result, columns=['Channel Name', 'Video Name', 'No of Comments']).reset_index(drop=True)
                df.index += 1
                return df  

            if select_question == '1. What are the names of all the videos and their corresponding channels?':
                st.dataframe(question1())
            elif select_question == '2. Which channels have the most number of videos, and how many videos do they have?':
                st.dataframe(question2())
                if st.button("Visulization"):
                    result = "Two"
            elif select_question == '3. What are the top 10 most viewed videos and their respective channels?':
                st.dataframe(question3())
            elif select_question == '4. How many comments were made on each video, and what are their corresponding video names?':
                st.dataframe(question4())
            elif select_question == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
                st.dataframe(question5())
            elif select_question == '6. What is the total number of likes for each video, and what are their corresponding video names?':
                st.dataframe(question6())
            elif select_question == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
                st.dataframe(question7())
                if st.button("Visulization"):
                    result = "seven"
            elif select_question == '8. What are the names of all the channels that have published videos in the year 2022?':
                st.dataframe(question8())
            elif select_question == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
                st.dataframe(question9())
            elif select_question == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
                st.dataframe(question10())
    except:
        pass

    try:
        with st.container():
                if result == "Two":
                    result1 = question2()  # Call the correct function to retrieve data
                    fig = px.bar(result1, x='Channel Name', y='Video Count', labels={'channel_name': 'Channel Name', 'video_count': 'Video Count'})
                    st.plotly_chart(fig)
                elif result == "seven":
                    result7 = question7()  # Call the correct function to retrieve data
                    fig = px.pie(result7,values='TotalViews',names='Channel Name')
                    st.plotly_chart(fig)
    except:
        pass                