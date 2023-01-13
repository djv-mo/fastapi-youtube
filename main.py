from fastapi import FastAPI
from download_video import download_video_router
from download_playlist import download_playlist_router

app = FastAPI()

app.include_router(download_video_router)
app.include_router(download_playlist_router)
