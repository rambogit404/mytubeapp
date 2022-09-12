import pymongo
import config_parser as cp

client: pymongo.MongoClient

MONGO_DB_URL=cp.getConfig("MONGO_DB_URL") #"mongodb+srv://yadmin:Test123@cluster0.ygatu.mongodb.net/?retryWrites=true&w=majority"


"""
    Initializing the Mongo db connection
"""


def init():
    try:
        global client
        client = pymongo.MongoClient(MONGO_DB_URL)
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
    text=''
    try:
        # Add validation data exist or not
        database = client['youtubedb']
        collection = database["youtube_comments"]
        commentsData=collection.find_one({"videoId":video_id})
        print(commentsData['commentsData'])
        comments=commentsData['commentsData']
        nl = '\n'
        for comment in comments:
            text = text+f"<Name>: {comment['commentorName']}{nl}"+f"<Comments>: {comment['commentText']}{nl}"


        print(text)
        return text
    except Exception as e:
        print("mongo_db: Mongo Database Error", e)
        return text

def close():
    client.close()

if __name__ == "__main__":
    init()
    print(fetchCommentsbyVideoId("2CRY5BYf-js11"))

