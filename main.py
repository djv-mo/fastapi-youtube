from fastapi import FastAPI
from download_video import download_video_router
from download_playlist import download_playlist_router
# from StreamDownload import download_stream_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(download_video_router)
app.include_router(download_playlist_router)
# app.include_router(download_stream_router)
