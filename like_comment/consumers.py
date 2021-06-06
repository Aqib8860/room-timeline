from starlette.endpoints import WebSocketEndpoint
from .models import LikeComment
from json import dump

class LikeCommentSocket(WebSocketEndpoint):
    encoding = 'json'

    async def on_connect(self, websocket):
        global ws 
        ws = websocket
        await ws.accept()
        global lc
        lc = LikeComment()

    async def on_receive(self, websocket, data):
        
        await ws.send_json(lc.get(data["video_id"]))

    def send(data):

        ws.send_json(lc.get(data["video_id"]))

    async def on_disconnect(self, websocket, close_code):
        await ws.close()
        lc.close()

