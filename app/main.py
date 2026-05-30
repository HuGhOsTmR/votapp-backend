from fastapi import FastAPI

from app.api.assembly_api import router as assembly_router
from app.models import *

from app.api.auth_api import router as auth_router
from app.api.admin_api import router as admin_router

from app.api.ws_api import router as ws_router

from fastapi.middleware.cors import CORSMiddleware
from app.api import assembly_api, motion_api



app = FastAPI(
    title="VotApp API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(ws_router)
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://votapp-frontend.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(assembly_api.router)
app.include_router(motion_api.router)
@app.get("/")
def home():

    return {
        "message": "VotApp funcionando correctamente"
    }

app.include_router(assembly_router)
