from starlette.routing import Route
from .views import getViews

views_urlpatterns=[
    Route('/views/{video_id:str}', getViews, methods=["GET"]),
]