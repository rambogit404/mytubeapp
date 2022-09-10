import mysql.connector as conn

DB_HOST_NAME = "localhost"
DB_USER = "root"
DB_PWD = "Test123"
mysql_db = ""
cursor = ""

"""
    Initializing the mysql db connection
"""


def init():
    global mysql_db, cursor
    mysql_db = conn.connect(host=DB_HOST_NAME, user=DB_USER, passwd=DB_PWD)
    cursor = mysql_db.cursor()


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


def saveVideoData(video_id, vurl, download_link, like, comment_count, video_title, thumbnail):
    try:
        # Add validation data exist or not
        video_title = video_title.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
        print(thumbnail)
        insert_qry = "insert into youtubedb.youtuber_data values('" + video_id + "','" + vurl + "','" + vurl + "','" + like + "','" + comment_count + "','" + video_title + "','" + thumbnail + "')"
        cursor.execute(insert_qry)
        mysql_db.commit()
    except Exception as e:
        print("Error : ", e)
