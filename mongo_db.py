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


def fetchCommentsbyVideoId(video_id):
    comments=[]
    try:
        # Add validation data exist or not
        database = client['youtubedb']
        collection = database["youtube_comments"]
        commentsData=collection.find_one({"videoId":video_id})
        print(commentsData['commentsData'])
        comments=commentsData['commentsData']
        return comments
    except Exception as e:
        print("mongo_db: Mongo Database Error", e)
        return comments

def close():
    client.close()

if __name__ == "__main__":
    init()
    print(fetchCommentsbyVideoId("2CRY5BYf-js11"))

