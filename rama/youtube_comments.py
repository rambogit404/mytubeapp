from googleapiclient.discovery import build
import mongo_db as db

API_KEY="AIzaSyCcTVNeWxkQObvTyvesPO0VhAGdIdx3xFQ"

def saveComments(video_id):

    try:
        # creating youtube resource object
        youtube = build('youtube', 'v3',
                        developerKey=API_KEY)
        #COTMO2sYJh0
        # retrieve youtube video results
        video_response = youtube. commentThreads().list(
                                    part="snippet,replies",
                                    videoId=video_id,
                                    maxResults= 1000,   #get 1000 comments
                                    order="orderUnspecified").execute()

       # print(video_response)
        #get first 10 items from 20 comments
        items = video_response["items"]
        comments = []
        replies = []
        print("------------------------------------------------------------------------------------------------------")
        for item in items:

            replies=[]
            item_info = item["snippet"]

            # the top level comment can have sub reply comments
            topLevelComment = item_info["topLevelComment"]
            comment_info = topLevelComment["snippet"]

            #print("Comment Id: ", topLevelComment['id'])
            #print("Comment By:", comment_info["authorDisplayName"])
            #print("Comment Text:", comment_info["textDisplay"])
            #print("Likes on Comment:", comment_info["likeCount"])
            #print("Comment Date: ", comment_info['publishedAt'])
            #print("================================\n")

            try:
                commentId= topLevelComment['id']

            except:
                commentId = 'No Comment Id'
            try:
                commenterName= comment_info['authorDisplayName']

            except:
                commenterName = 'No Commenter Name'
            try:
                commentText = comment_info['textDisplay']

            except:
                commentText = 'No Comment'

            try:
                replyItems = item['replies']['comments']
                for comment in replyItems:
                    try:
                        rcommentId = comment['id']

                    except:
                        rcommentId = "No Id"
                    try:
                        rcommentName = comment['snippet']['authorDisplayName']

                    except:
                        rcommentName = "No Name"

                    try:
                        rcommentText = comment['snippet']['textDisplay']

                    except:
                        rcommentText = "No Comment"

                    #print("----------Author name: ",rcommentName)
                    #print("----------Reply : ---------",rcommentText)
                    reply_dict = {"commentId": rcommentId, "commentorName": rcommentName, "commentText": rcommentText}
                    replies.append(reply_dict)

            except:
                reply="No Reply"

            #print("replies :",replies)
            commecnt_dic = {"commentId": commentId, "commentorName": commenterName, "commentText": commentText,
                            "reply": replies}
            comments.append(commecnt_dic)

        return_json = {"videoId": video_id, "commentsData": comments}

        db.saveCommentsData(return_json)
        print(return_json)
        return return_json
    except Exception as e:
        print("System Error ....",e.with_traceback())


if __name__ =="__main__":
    saveComments("COTMO2sYJh0")