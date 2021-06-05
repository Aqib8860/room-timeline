from starlette.routing import Route
from .views import uploadView, getVideo

videos_urlpatterns=[
    Route('/upload/', uploadView, methods=["POST"]),
    Route('/video/{id:str}', getVideo, methods=["GET"]),
]