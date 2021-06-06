from starlette.routing import Route
from .views import likeVideo, commentVideo, test

lc_urlpatterns=[
    Route('/like/', likeVideo, methods=["POST"]),
    Route('/comment/', commentVideo, methods=["POST"]),
    Route('/test/', test, methods=["POST"]),
]