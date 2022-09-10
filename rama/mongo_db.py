import pymongo

client=""

def init():
    global client
    client = pymongo.MongoClient(
        "mongodb+srv://yadmin:Test123@cluster0.ygatu.mongodb.net/?retryWrites=true&w=majority")




def saveCommentsData(data):
    try:
        # Add validation data exist or not
        database = client['youtubedb']
        collection = database["youtube_comments"]
        collection.insert_one(data)
    except Exception as e:
        print("Mongo Database Error", e.with_traceback())
