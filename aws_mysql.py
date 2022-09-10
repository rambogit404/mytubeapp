import mysql.connector as conn

DB_HOST_NAME = "mytubedb.cnaqs2xve1td.ap-south-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PWD = "MyTube123$"
PORT="3306"
REGION="ap-south-1b"
DBNAME="mytubedb"

mysql_db = ""
cursor = ""


# Initializing the mysql db connection

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


def TestInsertData():
    # global cursor
    try:
        insert_qry = "insert into mytubedb.mytube_data values (\"devtest\", \"devtest\", \"rama gaadi prj\", \"ytlink\", \"s3link\", \"ytd thumb\", \"23001\", \"393875\")"
        print('insert query prepared')
        cursor.execute(insert_qry)
        print('executed')
        mysql_db.commit()
        print('commited')
    except Exception as e:
        print("Error : ", e)

if __name__ == '__main__':
    init()
    TestInsertData()