from ffmpeg_streaming import Formats, Bitrate, Representation, Size, input
from starlette.responses import JSONResponse
from .models import BaseUpload
from datetime import datetime
from server.auth import jwt_authentication
from server.settings import AWS_BASE_URL,AWS_STORAGE_BUCKET_NAME, AWS_DEFAULT_ACL, s3Client, notify
from boto3 import client
from os import listdir, system
from threading import Thread


def videoConvertor(s3, video,profile_id,current_time, title, token):
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


    notify(token,message)


@jwt_authentication
async def uploadView(request):
    # import pdb; pdb.set_trace();
    try:
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
            thumbnail,
            ExtraArgs={"ACL": "public-read"}
        )

        system(f'rm {thumbnail}')

        video = f"media/Videos/Video{profile_id}_{current_time}.mp4"
        upload_video = await form["upload_file"].read()
        with open(video,"wb+") as f:
            f.write(upload_video)

        video_path=f"Videos/Video{profile_id}_{current_time}/Video{profile_id}_{current_time}.mpd"

        videos = BaseUpload()
        videos.create(
            profile_id,
            form['title'],
            form['description'],
            form['duration'],
            form['category'],
            AWS_BASE_URL+thumbnail[6:],
            AWS_BASE_URL+video_path,
            datetime.utcnow().timestamp()
        )

        token = videos.token(profile_id)

        optimizer_thread = Thread(target=videoConvertor, args=(s3, video,profile_id,current_time, form['title'], token))
        optimizer_thread.daemon = True
        optimizer_thread.start()
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

@jwt_authentication
async def deleteVideo(request):
    # import pdb; pdb.set_trace();
    try:
        video_id= request.path_params["id"]
        video=BaseUpload()
        video.delete(video_id)

        return JSONResponse({"message":"Video Deleted Successfully","status":True})

    except Exception as e:

        return JSONResponse({"message":str(e),"status":False},status_code=400)