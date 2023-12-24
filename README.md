# YouTube_Data_Harvesting_and_Warehousing
Introduction:

This project involves creating a user-friendly Streamlit application that utilizes the Google API to collect insightful data from YouTube channels. The acquired data is stored in MongoDB, then transitioned to a SQL data warehouse for analysis and exploration, all accessible through the Streamlit app.

Technologies Used:

* Python scripting
* Data Collection
* API integration
* Streamlit
* Data Management using MongoDB and SQL
* Plotly

Installation

To run this project, you need to install the following packages:

pip install google-api-python-client
pip install pymongo
pip install mysql.connector
pip install pandas
pip install streamlit
pip install plotly

Features

* Retrieve data from the YouTube API, including channel information, playlists, videos, and comments.
* Store the retrieved data in a MongoDB database.
* Option to check wheather the respective channel Data is exist or Not in MongoDb (Atlas).
* Migrate the data to a MySQL data warehouse.
* Analyze and visualize data using Streamlit and Plotly.
* Perform queries on the MySQL data warehouse.
* Display the list of channel name's along with subcription & view's count.

  
StreamLit app interface:

![image](https://github.com/lingesh20/YouTube_Data_Harvesting_and_Warehousing/assets/63338272/475202a7-7ddf-4fb2-9493-a5464af66399)
