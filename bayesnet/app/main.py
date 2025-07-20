# app/main.py
from fastapi import FastAPI
from app.api import networks

app = FastAPI()

app.include_router(networks.router, prefix="/networks")
