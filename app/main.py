from fastapi import FastAPI

from app.api.assembly_api import router as assembly_router
from app.models import *

from app.api.auth_api import router as auth_router
from app.api.admin_api import router as admin_router

from app.api.ws_api import router as ws_router

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="VotApp API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(ws_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://votapp-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.get("/")
def home():

    return {
        "message": "VotApp funcionando correctamente"
    }

app.include_router(assembly_router)
