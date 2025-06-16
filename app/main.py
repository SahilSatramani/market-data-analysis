from fastapi import FastAPI
from app.api.routes import router
from dotenv import load_dotenv

load_dotenv()
import os

app = FastAPI(title="Market Data Service")

app.include_router(router)
