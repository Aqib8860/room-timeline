from starlette.routing import Route
from .views import uploadView

videos_urlpatterns=[
    Route('/upload/', uploadView, methods=["POST"]),
]