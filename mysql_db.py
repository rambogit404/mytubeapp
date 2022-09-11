import mysql.connector as conn
from mysql.connector.cursor import MySQLCursor
import mongo_db as mdb

DB_HOST_NAME = "mytubedb.cnaqs2xve1td.ap-south-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PWD = "MyTube123$"


mysql_db = ""
cursor: MySQLCursor

"""
    Initializing the mysql db connection
"""


def init():
    try:
        global mysql_db, cursor
        mysql_db = conn.connect(host=DB_HOST_NAME, user=DB_USER, passwd=DB_PWD,auth_plugin='mysql_native_password')
        cursor = mysql_db.cursor()

    except Exception as e:
        print("mysql_db: init: Connection Error .. ")


"""
     Save the video Data in mysql Data base
    :rtype: object
    :param video_id: 
    :param vurl: 
    :param download_link: 
    :param like: 
    :param comment_count: 
    :param video_title: 
    :param thumbnail: 
    """


def saveVideoData(channel_id,video_id, vurl, download_link, like, comment_count, video_title, thumbnail):
    try:
        # Add validation data exist or not
        video_title = video_title.translate(
            {ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
        insert_qry = """
                    INSERT INTO mytubedb.mytube_data (channel_id,video_id,youtube_video_link,s3_download_link,likes_count,comments_count,tile_of_video,youtube_thumbnail_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """
        data = (channel_id, video_id, vurl, vurl, like, comment_count, video_title, thumbnail)

        cursor.execute(insert_qry, data)

        mysql_db.commit()
    except Exception as e:
        print("Error : ", e)


def close():
    cursor.close()
    mysql_db.close()


def fetchData(channel_id):
    videoData=[]
    try:
        cursor.execute("select video_id,youtube_thumbnail_url,youtube_video_link,s3_download_link,tile_of_video,"
                       "likes_count,comments_count from mytubedb.mytube_data where channel_id = '"+channel_id+"'")
        records = cursor.fetchall()
        for rec in records:
            recDic={"video_id":rec[0],"thumbnail":rec[1], "youtube_link":rec[2],"download_link":rec[3], "title":rec[4], "likes":rec[5], "comments_count":rec[6],"commentsData":mdb.fetchCommentsbyVideoId(rec[0])}
            videoData.append(recDic)
    except Exception as e:
        print("Error while fetching records",e)
    print("videoData : ", videoData)
    return videoData


if __name__ == "__main__":
    init()
    fetchData("UCNU_lfiiWBdtULKOw6X0Dig")