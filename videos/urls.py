from starlette.routing import Route
from .views import uploadView, getVideo, deleteVideo, videoTimeline, exploreImage

videos_urlpatterns=[
    Route('/upload/', uploadView, methods=["POST"]),
    Route('/explore/image', exploreImage, methods=["POST"]), 
    Route('/video/{id:str}', getVideo, methods=["GET"]),
    Route('/video/{id:str}', deleteVideo, methods=["DELETE"]),
    Route('/timeline/', videoTimeline, methods=["GET"]), 
]