import sys
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database import init_db
from auth import router as auth_router
from agent import router as agent_router

init_db()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOWED_ORIGIN", "http://127.0.0.1:8000")],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(agent_router)

@app.get("/")
def root():
    return FileResponse("frontend.html")


if __name__ == "__main__":
    uvicorn.run(app, port=8000, reload=False)