from pytube import Channel, YouTube
import s3_file_transfer as s3d3v
import youtube_comments as yc
import mysql_db as mydb
import config_parser as cp
import mongo_db as mdb

channel: Channel
max_vids = cp.getConfig("MAX_VID")

# initializing the Channel Object and mysql db
# arg1 passing channel url upto videos


def init(channel_url):
    global channel
    channel = Channel(channel_url)
    mydb.init()
    mdb.init()
    return channel


# Processing the Channel url and fetching all video informaiton
# arg1 passing file save path
def process_url(file_path="D:/"):
    try:
        download_link=''
        urls = channel.video_urls[:max_vids]
        channel_id = channel.channel_id
        for vurl in urls:

            yt = YouTube(vurl)
            try:

                video_title = yt.title
                thumbnail = yt.thumbnail_url
                print(video_title)
            except:
                video_title = 'No Title'

            try:

                like = yt.initial_data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']['videoActions']['menuRenderer']['topLevelButtons'][0]['toggleButtonRenderer']['defaultText'][
                    'simpleText']

            except:
                like = '0'

            try:
                comment_count = yt.initial_data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][
                    2]['itemSectionRenderer']['contents'][0]['commentsEntryPointHeaderRenderer']['commentCount']['simpleText']

            except:
                comment_count = '0'


            # Download the Video
            download_video(vurl, file_path)

            file_name_path = file_path + yt.video_id + ".mp4"

            # Uploading the videos to Cloud
            upld_res = upload_videos_to_s3(file_name_path)

             # Getting download link
            if upld_res[0]:
                download_link = upld_res[1]

            try:
                mydb.saveVideoData(channel_id, yt.video_id, vurl, download_link,
                                   like, comment_count, video_title, thumbnail)
            except Exception as e:
                print("Error while saving video Data....", e.with_traceback())

            try:
                yc.saveComments(yt.video_id)
            except:
                print("Error while saving Comments....")
    except:
        print("system Error!.....")

# Upload videos to s3 cloud memory
# arg1 Passing file save path


def upload_videos_to_s3(file_path):
    print(f'Uploading file: {file_path}')
    ret = s3d3v.upload_file(file_path, s3d3v.s3_bucket_name, True)
    print(f'ret: {ret}')
    return ret

# Download videos
# arg1 passing video url
# arg2 passing file save path


def download_video(url, file_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_by_itag(18)
        stream.download(output_path=file_path, filename=yt.video_id+".mp4")
    except:
        print("Error while download video:", url)

def close():
    mydb.close()
    mdb.close()

if __name__ == "__main__":
    print("Start : ")
    c_url = "https://www.youtube.com/user/Apple/videos"
    init(c_url)
    process_url()
