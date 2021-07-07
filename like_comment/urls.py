from starlette.routing import Route
from .views import likeVideo, commentVideo, getLikes, getComments, checkLike

lc_urlpatterns=[
    Route('/like/', likeVideo, methods=["POST"]),
    Route('/comment/', commentVideo, methods=["POST","DELETE"]),
    Route('/like/{id:str}',getLikes, methods=["GET"]),
    Route('/like/check/{video_id:str}',checkLike, methods=["GET"]),
    Route('/comment/{id:str}',getComments, methods=["GET"])
]