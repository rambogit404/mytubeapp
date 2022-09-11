import pymongo

client: pymongo.MongoClient

"""
    Initializing the Mongo db connection
"""


def init():
    try:
        global client
        client = pymongo.MongoClient(
            "mongodb+srv://yadmin:Test123@cluster0.ygatu.mongodb.net/?retryWrites=true&w=majority")
    except Exception as e:
        print("mongo_db: init: Connection error .... ")

"""
    :rtype: object
    :param data:  
"""


def saveCommentsData(data):
    try:
        # Add validation data exist or not
        database = client['youtubedb']
        collection = database["youtube_comments"]
        collection.insert_one(data)
    except Exception as e:
        print("mongo_db: Mongo Database Error", e)

def close():
    client.close()