from starlette.routing import Route
from .views import page_not_found
from videos.urls import videos_urlpatterns
from like_comment.urls import lc_urlpatterns

urlpatterns=[
    Route('/', page_not_found, methods=["GET","POST"]),
]

urlpatterns.extend(videos_urlpatterns)
urlpatterns.extend(lc_urlpatterns)
