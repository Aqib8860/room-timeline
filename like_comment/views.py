from starlette.responses import JSONResponse
from server.auth import jwt_authentication
from .models import Like, Comment

@jwt_authentication
async def likeVideo(request):

    try:

        profile_id = request.user_id

        data = await request.json()

        like = Like()

        res = like.create_or_delete(profile_id,data["video_id"])

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

        res = comment.create(profile_id,data["video_id"],data["comment"])

        comment.close()

        return JSONResponse({"message":res,"status":True})

    except Exception as e:

        return JSONResponse({"message":str(e),"status":False},status_code=400)
