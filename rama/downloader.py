from pytube import Channel, YouTube
import youtube_comments as yc
import mysql_db as mydb

channel = ""


# initializing the Channel Object and mysql db
# arg1 passing channel url upto videos
def init(channel_url):
    global channel
    channel = Channel(channel_url)
    mydb.init()
    yc.init()


# Processing the Channel url and fetching all video informaiton
# arg1 passing file save path
def process_url(file_path = "D:/"):
    try:
        urls = channel.video_urls[:50]

        for vurl in urls:

            yt = YouTube(vurl)
            try:

                video_title = yt.title
                thumbnail = yt.thumbnail_url
                print(video_title)
            except:
                video_title = 'No Title'

            try:

                like = yt.initial_data['contents'] \
                    ['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer'] \
                    ['videoActions']['menuRenderer']['topLevelButtons'][0]['toggleButtonRenderer']['defaultText'][
                    'simpleText']

            except:
                like = '0'

            try:
                comment_count = yt.initial_data['contents'] \
                    ['twoColumnWatchNextResults']['results']['results']['contents'][2]['itemSectionRenderer'] \
                    ['contents'][0]['commentsEntryPointHeaderRenderer']['commentCount']['simpleText']

            except:
                comment_count = '0'

            try:

                mydb.saveVideoData(yt.video_id, vurl, vurl, like, comment_count, video_title, thumbnail)
            except Exception as e:
                print("Error while saving video Data....", e.with_traceback())

            try:
                yc.saveComments(yt.video_id)
            except:
                print("Error while saving Comments....")

            # Download the Video
            download_video(vurl, file_path)

            file_name_path = file_path + video_title + ".mp4"

            # Uploading the videos to Cloud
            upload_videos_to_s3(file_name_path)
    except:
        print("system Error!.....")


# Upload videos to s3 cloud memory
# arg1 Passing file save path
def upload_videos_to_s3(file_path):
    print(file_path)


# Download videos
# arg1 passing video url
# arg2 passing file save path
def download_video(url, file_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_by_itag(18)
        stream.download(file_path)
    except:
        print("Error while download video:", url)


if __name__ == "__main__":
    print("Start : ")
    c_url = "https://www.youtube.com/user/krishnaik06/videos"
    init(c_url)
    process_url()
