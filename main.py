from starlette.applications import Starlette
import uvicorn
from server.urls import urlpatterns


app = Starlette(routes=urlpatterns)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="info", debug=True)
