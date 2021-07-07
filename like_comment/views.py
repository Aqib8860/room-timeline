from starlette.responses import JSONResponse
from server.auth import jwt_authentication
from .models import Like, Comment, LikeCommentView
from server.settings import group, notify

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
        if res == "Liked Successfully":
            cr,cn=like.creator_channel(data["video_id"])
            token=like.token(cr)
            notify(token,"{cn} liked your video")

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
            cr,cn=comment.creator_channel(data["video_id"])
            token=comment.token(cr)
            notify(token,"{cn} commented on your video")
            
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
