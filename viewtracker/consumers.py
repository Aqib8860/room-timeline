from starlette.endpoints import WebSocketEndpoint
from .models import ViewTracker
from like_comment.views import sendData

class ViewTrackingSocket(WebSocketEndpoint):
    
    encoding = 'json'

    async def on_connect(self, websocket):
        await websocket.accept()
        self.vt = ViewTracker()

    async def on_receive(self, websocket, data):
        try:

            # self.vt.roomTimeline(data["user_id"],data["limit"])
            
            await websocket.send_json(self.vt.roomTimeline(data["user_id"],data["limit"]))

            #self.vt.total(data["video_id"])

            #await sendData(data["video_id"])

        except Exception as e:
            await websocket.send_json({"message":str(e)})


    async def on_disconnect(self, websocket, close_code):
        await websocket.close()
        self.vt.close()
