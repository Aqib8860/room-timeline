from starlette.responses import JSONResponse
from server.auth import jwt_authentication
from .models import Like, Comment, LikeCommentView
from server.settings import group
import requests

async def sendData(video_id):
    
    lcv = LikeCommentView()
    await group.group_send("video", data=lcv.get(video_id))

    lcv.close()

@jwt_authentication
async def likeVideo(request):

    try:

        profile_id = request.user_id
        data = await request.json()

        like = Like()

        res = like.create_or_delete(profile_id,data["video_id"])

        await sendData(data["video_id"])

        if res == "Liked Successfully":

            token = request.headers['authorization'].split(" ")[1]
            message=f"{like.user_name(profile_id)} liked your video {like.video_title(data['video_id'])}"
            requests.get(f"http://52.91.187.209:8000/notification/{token}/{message}")

        like.close()


        return JSONResponse({"message":res,"status":True})

    except Exception as e:

        return JSONResponse({"message":str(e),"status":False},status_code=400)

@jwt_authentication
async def commentVideo(request):

    try:

        profile_id = request.user_id

        data = await request.json()

        comment = Comment()

        if request.method == 'POST':

            res = comment.create(profile_id,data["video_id"],data["comment"])
            token = request.headers['authorization'].split(" ")[1]
            message=f"{comment.user_name(profile_id)} commented on your video {comment.video_title(data['video_id'])}"
            requests.get(f"http://52.91.187.209:8000/notification/{token}/{message}")

        else:
    
            res = comment.delete(data["video_comment_id"],data["comment_id"])


        comment.close()

        await sendData(data["video_id"])

        return JSONResponse({"message":res,"status":True})

    except Exception as e:

        return JSONResponse({"message":str(e),"status":False},status_code=400)
