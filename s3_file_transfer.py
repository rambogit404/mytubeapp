from botocore.exceptions import ClientError
import logging
from distutils.command.upload import upload
from mimetypes import init
import boto3
import glob
import os
import random
import config_parser as cpp

s3_bucket_name = cpp.getConfig('S3_BUCKET_NAME') #'youtube-videos-04092022'
s3_client = None

def init_aws_s3_client():
    global s3_client
    try:
        s3_client = boto3.client('s3')
    except:
        print('exception occured')


def get_aws_s3_client():
    global s3_client
    if s3_client is None:
        init_aws_s3_client()
    return s3_client

# upload file
# param: video_file_name : absolute path of the file to be uploaded
# param: bucket_name: s3 bucket name 
# param: get_public_url: get public url of the uploaded object
# returns tuple of {upload status, public_url}
def upload_file(video_file_name, bucket_name=s3_bucket_name, public_url=False):
    object_name = os.path.basename(video_file_name)
    print(f'Object name: {object_name}')
    link = None
    try:
        print('uploading...')
        response = get_aws_s3_client().upload_file(
            video_file_name, bucket_name, object_name)

        if public_url:
            link = get_public_url(object_name)
            # print(link)
    except ClientError as e:
        print(e)
        return (False,None)
    return (True, link)

def upload_test():
    for file in glob.glob("C:\\Users\\deven\\Desktop\\upld\\*.*"):
        print(f'Uploading file: {file}')
        retVal = upload_file(file, s3_bucket_name, True)
        print(f'{retVal}')
    return

# download file
# param: video_file_name : name of the video file object to download (just the name with extensiton)
# param: destination: destination dir to store, defaults to current dir
# returns Nothing
def download(video_file_name, destination='./'):
    get_aws_s3_client().download_file(s3_bucket_name, video_file_name, os.path.join(
        destination, video_file_name))
    return


def download_test():
    files_list = [file for file in glob.glob(
        "C:\\Users\\deven\\Desktop\\upld\\*.*")]
    files = [os.path.basename(file) for file in files_list]
    for i in range(4):
        rfile = random.choice(files)
        print(f'downloading file... {rfile}')
        download(rfile, "C:\\Users\\deven\\Desktop\\dld")
        resp = get_public_url(rfile)
        print(f'public url: {resp}')
    return

# creates a temporary download url with public access
# param: object_name: name of the file to generate the link
# param: expiration: url expiration time in seconds
# returns the url
# 604799 is a week in seconds
def get_public_url(object_name, expiration=604799):

    try:
        response = get_aws_s3_client().generate_presigned_url('get_object',
                                                              Params={'Bucket': s3_bucket_name,
                                                                      'Key': object_name},
                                                              ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return response

if __name__ == '__main__':
    print('begin')
    print('testing upload')
    upload_test()
    # print('testing download')
    # download_test()
    print('done')
