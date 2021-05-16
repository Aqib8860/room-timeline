from starlette.applications import Starlette
import uvicorn
from server.urls import urlpatterns

app = Starlette(routes=urlpatterns)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", debug=True)