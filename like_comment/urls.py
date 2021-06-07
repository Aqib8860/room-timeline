from starlette.routing import Route
from .views import likeVideo, commentVideo

lc_urlpatterns=[
    Route('/like/', likeVideo, methods=["POST"]),
    Route('/comment/', commentVideo, methods=["POST","DELETE"]),
]