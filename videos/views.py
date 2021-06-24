from ffmpeg_streaming import Formats, Bitrate, Representation, Size, input
from starlette.responses import JSONResponse
from .models import BaseUpload
from datetime import datetime
from server.auth import jwt_authentication
from server.settings import AWS_BASE_URL,AWS_STORAGE_BUCKET_NAME, AWS_DEFAULT_ACL, s3Client
from boto3 import client
from os import listdir, system
from threading import Thread
import requests

def videoConvertor(s3, video,profile_id,current_time, token, title):
    output = f"Videos/Video{profile_id}_{current_time}/"
    _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    dash = input(video).dash(Formats.h264())
    dash.representations(_480p)
    dash.output(f"media/{output}Video{profile_id}_{current_time}.mpd")
    system(f'rm {video}')
    for file in listdir(f'media/Videos/Video{profile_id}_{current_time}/'):
        
        s3.upload_file(
            f"media/{output}{file}",
            AWS_STORAGE_BUCKET_NAME,
            f"{output}{file}",
            ExtraArgs={"ACL": "public-read"}
        )

        system(f'rm media/{output}{file}')
    system(f'rm -rf media/{output}')

    message=f"{title} Uploaded Successfully"

    requests.get(f"http://13.235.67.71/notification/{profile_id}/Video Upload/{id}/{message}")


@jwt_authentication
async def uploadView(request):
    # import pdb; pdb.set_trace();
    try:
        token = request.headers['authorization'].split(" ")[1]

        profile_id= request.user_id

        form = await request.form()
        current_time=int(datetime.utcnow().timestamp())
        thumbnail = f"media/Video_Thumbnails/Thumbnail{profile_id}_{current_time}.jpg"

        upload_thumbnail = await form["thumbnail"].read()
        with open(thumbnail,"wb+") as f:
            f.write(upload_thumbnail)

        s3 = s3Client()
        s3.upload_file(
            thumbnail,
            AWS_STORAGE_BUCKET_NAME,
            thumbnail[6:],
            ExtraArgs={"ACL": "public-read"}
        )

        system(f'rm {thumbnail}')

        video = f"media/Videos/Video{profile_id}_{current_time}.mp4"
        upload_video = await form["upload_file"].read()
        with open(video,"wb+") as f:
            f.write(upload_video)

        video_path=f"Videos/Video{profile_id}_{current_time}/Video{profile_id}_{current_time}.mpd"
        
        optimizer_thread = Thread(target=videoConvertor, args=(s3, video,profile_id,current_time,token, form['title']))
        optimizer_thread.daemon = True
        optimizer_thread.start()

        video = BaseUpload()
        video.create(
            profile_id,
            form['title'],
            form['description'],
            form['duration'],
            form['category'],
            AWS_BASE_URL+thumbnail[6:],
            AWS_BASE_URL+video_path,
            datetime.utcnow().timestamp()
        )

        return JSONResponse({"message":"Video Uploaded Successfully","status":True})

    except Exception as e:

        return JSONResponse({"message":str(e),"status":False},status_code=400)


async def getVideo(request):
    # import pdb; pdb.set_trace();
    try:

        id = request.path_params["id"]
        
        video = BaseUpload()

        data = video.get(id)

        return JSONResponse({"message":"Success","data":data,"status":True})

    except Exception as e:

        return JSONResponse({"message":str(e),"status":False},status_code=400)
