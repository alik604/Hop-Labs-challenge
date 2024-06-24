from api.routes import detections
# from routes import detections # uses this lets the tests work but then Main.py breaks...
## TODO should this be `from routes import detections`? Importing this file for tests doesnt work too well
# Even PyCharm says the above is wrong

from fastapi import FastAPI


app = FastAPI(title="challenge", docs_url="/")
app.include_router(detections.router, prefix="/detections")
