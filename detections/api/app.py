from api.routes import detections

from fastapi import FastAPI


app = FastAPI(title="challenge", docs_url="/")
app.include_router(detections.router, prefix="/detections")
