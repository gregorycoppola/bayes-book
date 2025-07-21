# app/main.py
from fastapi import FastAPI
from app.api import networks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ✅ Allow your Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(networks.router, prefix="/networks")
    