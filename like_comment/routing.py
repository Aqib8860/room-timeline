from .consumers import LikeCommentSocket
from starlette.routing import WebSocketRoute

lc_socketpatterns=[
    WebSocketRoute("/ws/lc", LikeCommentSocket),
]
