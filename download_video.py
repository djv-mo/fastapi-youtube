from fastapi import APIRouter, Query
from pydantic import HttpUrl
from pytube import YouTube

download_video_router = APIRouter()


@download_video_router.get("/download/{url:path}")
async def download_video(url: HttpUrl, format: str = Query(..., title='Video Format', description='Choose the format of the video',
                                                           choices=["mp3", "mp4"])):
    yt = YouTube(url)
    title = yt.title
    thumbnail = yt.thumbnail_url
    duration = yt.length
    if format == 'mp4':
        mp4_streams = yt.streams.filter(progressive=True)
        mp4 = {}
        for stream in mp4_streams:
            mp4[stream.itag] = {'resolution': stream.resolution,
                                'size_in_mb': stream.filesize_mb,
                                'download_url': stream.url}

        return {"title": title, 'thumbnail': thumbnail,
                'duration': duration, 'streams': mp4}
    elif format == 'mp3':
        mp3_streams = yt.streams.get_audio_only()

        mp3 = {'abr': mp3_streams.abr,
               'size_in_mb': mp3_streams.filesize_mb,
               'audio_codec': mp3_streams.audio_codec.split(".")[0],
               'download_url': mp3_streams.url}

        return {"title": title, 'thumbnail': thumbnail,
                'duration': duration, 'streams': mp3}
