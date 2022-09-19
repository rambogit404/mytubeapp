from googleapiclient.discovery import build
import mongo_db as db
import config_parser as cp

API_KEY = cp.getConfig("API_KEY") #"AIzaSyCcTVNeWxkQObvTyvesPO0VhAGdIdx3xFQ"


def saveComments(video_id):
    """
    Extracting Comments and Replies with video id using google api
    :param video_id:
    """
    try:
        # creating youtube resource object
        youtube = build('youtube', 'v3',
                        developerKey=API_KEY)
        video_response = None
        try:
            # retrieve youtube video results
            video_response = youtube. commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=2000,  # get 1000 comments
                order="orderUnspecified").execute()
        except Exception as e:
            print("youtube_comments: savecomments: while fetching comments getting error ")
        comments = []
        if video_response!=None:
            # get first 10 items from 20 comments
            items = video_response["items"]

            replies = []
            # print("------------------------------------------------------------------------------------------------------")
            for item in items:

                replies = []
                item_info = item["snippet"]

                # the top level comment can have sub reply comments
                topLevelComment = item_info["topLevelComment"]
                comment_info = topLevelComment["snippet"]

                try:
                    commentId = topLevelComment['id']

                except:
                    commentId = 'No Comment Id'
                try:
                    commenterName = comment_info['authorDisplayName']

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
                        reply_dict = {
                            "commentId": rcommentId, "commentorName": rcommentName, "commentText": rcommentText}
                        replies.append(reply_dict)
                        # print(replies)
                except:
                    reply = "No Reply"

                #print("replies :",replies)
                commecnt_dic = {"commentId": commentId, "commentorName": commenterName, "commentText": commentText,
                                "reply": replies}
                comments.append(commecnt_dic)
        else:
            comments

        return_json = {"videoId": video_id, "commentsData": comments}

        db.saveCommentsData(return_json)
        # print(return_json)

    except Exception as e:
        print("youtube_comments: saveComments: System Error ....", e)


if __name__ == "__main__":
    db.init()
    saveComments("COTMO2sYJh0")
