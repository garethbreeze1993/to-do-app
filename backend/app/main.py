import configparser
import logging
import logging.config
from fastapi import FastAPI, Depends

from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.routers import users, auth, tasks, reports
from app import oauth2, models

app = FastAPI()
# command uvicorn app.main:app to run server

config = configparser.ConfigParser()
config.read('logging.ini')
logging.config.fileConfig(config)

log = logging.getLogger(__name__)

# At the moment allow all domains and all headers to connect to this API maybe change when push to deployment etc.
origins = ["*"]  # This means all domains can access our API

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(reports.router)

add_pagination(app)


@app.get("/")
def read_root(current_user: 'models.User' = Depends(oauth2.get_current_user)):
    return {"Hello": "World"}
