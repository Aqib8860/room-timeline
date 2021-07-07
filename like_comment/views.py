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
        like=Like()
        res = like.create_or_delete(profile_id,data["video_id"])
        await sendData(data["video_id"])

        #if res == "Liked Successfully":
#            title, creator = like.video_details(data['video_id'])
#            message=f"{like.user_name(profile_id)} liked your video {title}"
#            vid=data['video_id']
#            requests.get(f"http://13.235.67.71/notification/{creator}/Like/{vid}/{message}")
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
#            title, creator = comment.video_details(data['video_id'])
#            vid=data['video_id']
#            message=f"{comment.user_name(profile_id)} commented on your video {title}"
#            requests.get(f"http://13.235.67.71/notification/{creator}/Comment/{vid}/{message}")
            
        else:
        
            res = comment.delete(data["video_comment_id"],data["comment_id"])


        comment.close()

        await sendData(data["video_id"])

        return JSONResponse({"message":res,"status":True})

    except Exception as e:

        return JSONResponse({"message":str(e),"status":False},status_code=400)

async def getLikes(request):
    try:
        data = request.path_params["id"]
        like = Like()
        res = like.getLike(data)
        like.close()
        return JSONResponse({"message":"Success","data":res,"status":True},status_code=200)
    except Exception as e:
        return JSONResponse({"message":str(e),"status":False}, status_code=400)

async def getComments(request):
    try:
        data = request.path_params["id"]
        comment = Comment()
        res = comment.getComment(data)
        comment.close()
        return JSONResponse({"message":"Success","data":res,"status":True})
    except Exception as e:
        return JSONResponse({"message":str(e),"status":False}, status_code=400)

@jwt_authentication
async def checkLike(request):
    try:
        video_id=request.path_params["video_id"]
        profile_id=request.user_id
        like=Like()
        res=like.checkLike(video_id,profile_id)
        like.close()
        return JSONResponse({"message":"Success","data":res,"status":True})
    except Exception as e:
        return JSONResponse({"message":str(e), "status":False}, status_code=400)
