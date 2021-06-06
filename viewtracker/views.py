from starlette.responses import JSONResponse
from .models import ViewTracker

async def getViews(request):
    # import pdb; pdb.set_trace();
    try:

        video_id = request.path_params["video_id"]
        
        views = ViewTracker()

        data = views.get(video_id)

        views.close()

        return JSONResponse({"message":"Success","data":data,"status":True})

    except Exception as e:

        return JSONResponse({"message":str(e),"status":False},status_code=400)
