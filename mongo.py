import pymongo as db 

url = "mongodb://localhost:27017/"
db_name = "youtube"
client = db.MongoClient(url)
database = client[db_name]
collection_name = "youtubedata"

def store_function(channel_data):

    collection = database[collection_name]
    result = collection.insert_one(channel_data)
    print(f"Inserted document ID: {result.inserted_id}")
    client.close()
    return "Data stored successfully in MongoDB"


def find_function(channelId):

    collection = database[collection_name]
    result = collection.find_one({'Channel_Name.channel_id': channelId})
    client.close()
    return result